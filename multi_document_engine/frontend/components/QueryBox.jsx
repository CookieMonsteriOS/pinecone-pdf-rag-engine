import { useState } from 'react';
import axios from 'axios';

export default function QueryBox({ onResults }) {
  const [query, setQuery] = useState('');
  const [loading, setLoading] = useState(false);

  const handleQuery = async (e) => {
    e.preventDefault();
    if (!query) return;
    setLoading(true);
    try {
      const res = await axios.get(`http://localhost:8000/query`, {
        params: { q: query, top_k: 5 },
      });
      onResults(res.data);
      console.log(res.data);
    } catch (err) {
      alert('Query error: ' + (err.response?.data?.error || err.message));
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleQuery} className="bg-white rounded shadow p-4 flex items-center space-x-2">
      <input
        className="flex-1 border border-gray-300 rounded px-3 py-2 focus:outline-none focus:ring"
        type="text"
        placeholder="Enter your query..."
        value={query}
        onChange={e => setQuery(e.target.value)}
        disabled={loading}
      />
      <button
        className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 font-semibold"
        type="submit"
        disabled={loading}
      >
        {loading ? 'Searching...' : 'Search'}
      </button>
    </form>
  );
}
