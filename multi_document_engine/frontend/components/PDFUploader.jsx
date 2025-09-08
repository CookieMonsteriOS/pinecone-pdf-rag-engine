import axios from 'axios';

export default function PDFUploader({ onProcessed }) {
  const handleProcess = async () => {
    try {
      const res = await axios.get('http://localhost:8000/process-pdfs');
      onProcessed(res.data);
    } catch (err) {
      alert('Error processing PDFs: ' + (err.response?.data?.error || err.message));
    }
  };

  return (
    <div className="bg-white rounded shadow p-4 flex flex-col items-center">
      <button
        onClick={handleProcess}
        className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 font-semibold"
      >
        Process PDFs
      </button>
    </div>
  );
}
