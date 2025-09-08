# Pinecone PDF RAG Engine

[![Python Version](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-v0.111-green)](https://fastapi.tiangolo.com/)
[![Pinecone](https://img.shields.io/badge/Pinecone-v2025.04-purple)](https://www.pinecone.io/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![GitHub stars](https://img.shields.io/github/stars/<your-username>/pinecone-pdf-rag-engine?style=social)](https://github.com/<your-username>/pinecone-pdf-rag-engine/stargazers)

AI-powered PDF Retrieval-Augmented Generation (RAG) engine that ingests PDFs, chunks them, generates embeddings, and enables semantic search via Pinecone. Built with Python, FastAPI, Pinecone, and React.

## 🚀 Features
- 📄 Multi-page PDF ingestion and chunking
- 🤖 Embedding generation using **SentenceTransformers**
- 📦 Vector storage and retrieval using **Pinecone**
- 🔎 Semantic search with top-k relevant chunks
- 🖥️ Minimal **React frontend** for querying and visualization
- ⚡ FastAPI backend serving API endpoints for processing PDFs and querying

## 📦 Tech Stack
- Python 3.11+
- FastAPI
- SentenceTransformers
- Pinecone
- React 18+
- Axios (for frontend API calls)
- Node.js 18+

## 📈 Use Cases
- Document retrieval for research papers or corporate documents
- Knowledge base search for internal PDFs
- Demonstration of RAG pipelines for AI-first startups
- Rapid prototyping of semantic search interfaces

## Project Structure

multi_document_engine/
├── backend/
│ ├── app.py # FastAPI application
│ ├── embeddings/ # Embedding model loader and vectorization
│ ├── chunking/ # Document chunking utilities
│ ├── loaders/ # PDF loader
│ ├── pinecone_client/ # Pinecone integration
│ └── data/pdfs/ # Example PDFs
├── frontend/ # React frontend
│ └── ... # React components and pages
└── requirements.txt # Python dependencies

## 🛠️ Installation

Clone the repository and navigate into the project:

```bash
git clone https://github.com/<your-username>/pinecone-pdf-rag-engine.git
cd pinecone-pdf-rag-engine/multi_document_engine

Backend Setup

1. (Optional) Create and activate a virtual environment:
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

2. Install Python dependencies:
pip install -r backend/requirements.txt

3. Create a .env file inside backend/ with your Pinecone credentials:
PINECONE_API_KEY=<your-pinecone-api-key>
PINECONE_ENV=<your-pinecone-environment>

4. Run the FastAPI backend:
cd backend
uvicorn app:app --reload

The backend will run at http://localhost:8000

Available API Endpoints:

/ → Health check

/process-pdfs → Load PDFs, generate embeddings, upsert vectors to Pinecone

/query?q=<your-query> → Retrieve top-k relevant chunks

Frontend Setup

1. Navigate to the frontend folder:

cd ../frontend

2. Install Node.js dependencies:

npm install

3. Start the React app:

npm start

The frontend will run at http://localhost:3000 . Use the input box and button to query the RAG engine.

📝 Usage

Place your PDFs in backend/data/pdfs/

Run /process-pdfs to ingest PDFs and upsert embeddings

Query the RAG engine via /query or the React frontend

Retrieve top-k relevant chunks with metadata for analysis

⚡ Notes

Ensure EMBEDDING_DIM matches your embedding model (default: 384 for all-MiniLM-L6-v2)

CORS is enabled in FastAPI to allow local React integration

The frontend is minimal and designed for demonstration; can be extended for production use. 



