# 👗 AI-Powered Fashion Review Search

An intelligent review search system that leverages sentence embeddings and topic modelling to explore and rank customer reviews from a clothing dataset. This application enables users to search reviews by custom text queries or predefined topics like **quality**, **fit**, **size**, **comfort**, and **price** — all categorized by clothing classes.

---

## 🚀 Features

- 🔍 **Search by Text Query**: Enter any custom query and retrieve semantically similar reviews.
- 🗂️ **Search by Topic**: Select from predefined topics (e.g., quality, fit) to see the most relevant reviews.
- 🏷️ **Class Metadata Included**: Each review result is tagged with its corresponding clothing class name.
- ⚡ **Fast and Scalable**: Powered by Sentence Transformers and ChromaDB for rapid semantic search.
- 🔧 **Interactive Frontend**: React-based UI to interact with the FastAPI backend.

---

##  Tech Stack

- **Backend**: FastAPI, SentenceTransformers (`all-MiniLM-L6-v2`), Scikit-learn, ChromaDB
- **Frontend**: React (Vite)
- **Data**: Clothing review dataset with attributes like `Review Text`, `Title`, `Class Name`, etc.
- **Deployment Ready**: CORS enabled, async lifecycle, batch processing supported

---

## 📦 Installation

## ✨ Acknowledgments
Hugging Face SentenceTransformers

ChromaDB

FastAPI

### Backend (FastAPI)

1. **Clone the repo**
   ```bash
   git clone https://github.com/yourusername/fashion-review-search.git
   cd fashion-review-search/backend

### Frontend (React)
```bash
cd ../frontend
npm install
npm run dev

![Alt text](UI_1.jpeg)

