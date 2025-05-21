import { useState } from "react";
import axios from "axios";
import "./App.css"; // Importing custom CSS file

function App() {
  const [mode, setMode] = useState("text"); // 'text' or 'topic'
  const [query, setQuery] = useState("");
  const [topic, setTopic] = useState("");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSearch = async () => {
    setLoading(true);
    setError("");
    setResults([]);

    try {
      if (mode === "text") {
        const res = await axios.post("http://localhost:8000/search_by_text", {
          query,
          top_n: 5,
        });
        setResults(res.data.results);
      } else if (mode === "topic") {
        const res = await axios.get(`http://localhost:8000/search_by_topic`, {
          params: { topic, top_n: 5 },
        });
        setResults(res.data.top_reviews);
      }
    } catch (err) {
      setError("Failed to fetch results. Please try again.", err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container my-5">
      <h1 className="text-center mb-4"> SmartReview: AI for Clothing Insights</h1>

      <div className="d-flex justify-content-center mb-4">
        <button 
          onClick={() => setMode("text")}
          className={`btn ${
            mode === "text" ? "btn-primary" : "btn-light"
          } mx-2`}
        >
          Search by Text
        </button>
        <button
          onClick={() => setMode("topic")}
          className={`btn ${
            mode === "topic" ? "btn-primary" : "btn-light"
          } mx-2`}
        >
          Search by Topic
        </button>
      </div>

      <div className="d-flex justify-content-center mb-4">
        {mode === "text" ? (
          <input
            type="text"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="form-control w-50"
            placeholder="Type your review..."
          />
        ) : (
          <input
            type="text"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            className="form-control w-50"
            placeholder="Enter topic like 'fit', 'comfort'..."
          />
        )}
        <button
          onClick={handleSearch}
          className="btn btn-success ml-2"
          disabled={loading}
        >
          {loading ? "Searching..." : "Search"}
        </button>
      </div>

      {error && <p className="text-danger text-center">{error}</p>}

      <ul className="list-group">
        {results.map((r, i) => (
          <li key={i} className="list-group-item">
            <div>
              <h5 className="mb-1">{r.class_name}</h5>
              <p className="mb-0">{r.review}</p>
            </div>
          </li>
        ))}
      </ul>
    </div>
  );
}

export default App;
