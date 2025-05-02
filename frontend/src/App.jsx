import { useState } from 'react';
import './App.css';
import axios from 'axios';

function App() {
  const [url, setUrl] = useState('');
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const backendUrl = "http://localhost:8000/search";

  const handleSearch = async () => {
    if (!url || !query) {
      setError("Both URL and query are required.");
      return;
    }

    setLoading(true);
    setError('');
    setResults([]);

    try {
      const res = await axios.post(backendUrl, { url, query });
      setResults(res.data.matches);
    } catch (err) {
      setError(err.response?.data?.detail || "An error occurred.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container">
      <h1>Semantic Search</h1>

      <div className="input-group">
        <input
          type="text"
          placeholder="Enter URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
        />
        <input
          type="text"
          placeholder="Enter query"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
        />
        <button onClick={handleSearch} disabled={loading}>
          {loading ? "Searching..." : "Search"}
        </button>
      </div>

      {error && <p className="error">{error}</p>}

      {results.length > 0 && (
        <div className="results">
          <h2>Top Matches</h2>
          {results.map((match, idx) => (
            <div key={idx} className="result-card">
              <p><strong>Chunk:</strong> {match.chunk}</p>
              <p><strong>URL:</strong> {match.url}</p>
              <p><strong>Score:</strong> {match.score.toFixed(4)}</p>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default App;
