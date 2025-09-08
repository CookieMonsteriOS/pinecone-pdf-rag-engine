import './index.css';
import PDFUploader from './components/PDFUploader';
import QueryBox from './components/QueryBox';
import ResultsList from './components/ResultsList';
import { useState } from 'react';

export default function App() {
  const [chunksInfo, setChunksInfo] = useState(null);
  const [results, setResults] = useState([]);

  return (
    <div className="min-h-screen bg-gray-50 p-4">
      <div className="max-w-2xl mx-auto space-y-6">
        <h1 className="text-3xl font-bold text-center mb-6">Multi-Document Insight Engine</h1>
        <PDFUploader onProcessed={setChunksInfo} />
        {chunksInfo && (
          <div className="bg-white rounded shadow p-4">
            <div className="font-semibold mb-2">Total Chunks: {chunksInfo.total_chunks}</div>
            <div>
              <div className="font-semibold">Preview (first 5 chunks):</div>
              <ul className="list-disc pl-5">
                {chunksInfo.preview.map((chunk, i) => (
                  <li key={i} className="mb-2">
                    <div className="text-sm text-gray-700 whitespace-pre-line">
                      <b>Document:</b> {chunk.document}, <b>Page:</b> {chunk.page}
                      <br/>
                      <b>Text:</b> {chunk.text?.slice(0, 300) || chunk}
                    </div>
                  </li>
                ))}
              </ul>
            </div>
          </div>
        )}
        <QueryBox onResults={setResults} />
        <ResultsList results={results} />
      </div>
    </div>
  );
}
