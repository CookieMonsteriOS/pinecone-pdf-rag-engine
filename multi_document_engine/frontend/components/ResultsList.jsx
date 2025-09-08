export default function ResultsList({ results }) {
  if (!results?.length) return null;
  return (
    <div className="bg-white rounded shadow p-4">
      <h2 className="text-lg font-bold mb-2">Results</h2>
      <ul className="divide-y divide-gray-200">
        {results.map((r, i) => (
          <li key={r.id || i} className="py-3">
            <div className="text-gray-800 mb-1">
              <b>Document:</b> {r.metadata?.document}, <b>Page:</b> {r.metadata?.page}
            </div>
            <div className="text-gray-600 mb-1 whitespace-pre-line">
              <b>Text:</b> {r.metadata?.text?.slice(0, 400) || '(no text)'}
            </div>
            <div className="text-xs text-gray-500">Score: {r.score?.toFixed(3)}</div>
          </li>
        ))}
      </ul>
    </div>
  );
}
