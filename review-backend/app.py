from fastapi import FastAPI, Query, Request
from sentence_transformers import SentenceTransformer
import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import chromadb
from chromadb.config import Settings
from pydantic import BaseModel
from typing import Optional
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware

TOPICS = ['quality', 'fit', 'size', 'comfort', 'price']


@asynccontextmanager
async def lifespan(app: FastAPI):
    model = SentenceTransformer('all-MiniLM-L6-v2')

    reviews = pd.read_csv("Data.csv")
    filtered_reviews = reviews[reviews['Review Text'].notnull()]
    review_text = filtered_reviews['Review Text'].tolist()
    class_names = filtered_reviews['Class Name'].tolist()
    review_embeddings = model.encode(review_text, show_progress_bar=True)

    topics_embeddings = model.encode(TOPICS, show_progress_bar=True)
    similarities = cosine_similarity(review_embeddings, topics_embeddings)

    chroma_client = chromadb.Client(Settings(anonymized_telemetry=False))
    collection = chroma_client.create_collection(name="reviews")

    batch_size = 5000
    for i in range(0, len(review_text), batch_size):
        batch_texts = review_text[i:i+batch_size]
        batch_embeddings = review_embeddings[i:i+batch_size].tolist()
        batch_ids = [f"review_{j}" for j in range(i, i+len(batch_texts))]
        batch_class_names = class_names[i:i+batch_size]
        batch_metadatas = [{"Class Name": cn} for cn in batch_class_names]

        collection.add(documents=batch_texts,
                       embeddings=batch_embeddings,
                       ids=batch_ids,
                       metadatas=batch_metadatas)

    app.state.model = model
    app.state.review_text = review_text
    app.state.review_embeddings = review_embeddings
    app.state.topics = TOPICS
    app.state.topics_embeddings = topics_embeddings
    app.state.similarities = similarities
    app.state.collection = collection
    app.state.class_names = class_names

    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    query: str
    top_n: Optional[int] = 3


@app.get("/")
def root():
    return {"message": "Welcome to the Review Search API!"}


@app.post("/search_by_text")
def search_by_text(payload: QueryRequest, request: Request):
    model = request.app.state.model
    collection = request.app.state.collection

    query_emb = model.encode([payload.query])
    results = collection.query(
        query_embeddings=query_emb, n_results=payload.top_n, include=['documents', 'metadatas'])

    combined_results = []
    for review, metadata in zip(results['documents'][0], results.get('metadatas', [{}])[0]):
        class_name = metadata.get("Class Name") if metadata else "Unknown"
        combined_results.append({
            "review": review,
            "class_name": class_name
        })

    return {
        "query": payload.query,
        "results": combined_results
    }


@app.get("/search_by_topic")
def search_by_topic(request: Request,
                    topic: str = Query(...,
                                       description="One of: quality, fit, size, comfort, price"),
                    top_n: int = 5):

    topics = request.app.state.topics
    review_text = request.app.state.review_text
    similarities = request.app.state.similarities
    class_names = request.app.state.class_names

    if topic not in topics:
        return {"error": f"Invalid topic. Choose from {topics}"}

    topic_index = topics.index(topic)
    topic_scores = similarities[:, topic_index]
    top_indices = np.argsort(topic_scores)[-top_n:][::-1]

    top_results = [
        {"class_name": class_names[i], "review": review_text[i]}
        for i in top_indices
    ]

    return {"topic": topic, "top_reviews": top_results}
