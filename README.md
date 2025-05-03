# 🔍 Semantic Search with Weaviate and Sentence Embeddings

This project demonstrates how to build a semantic search system using **Weaviate** and **Sentence Transformers** to retrieve contextually relevant content from web pages. It processes raw HTML from any given URL, cleans and chunks the content, generates embeddings, and stores them in Weaviate for fast and efficient semantic querying.

---

## 🚀 Project Overview

### 🧠 Backend – FastAPI
The FastAPI backend handles:
- 🔗 Fetching HTML content from a given URL
- 🧹 Cleaning and chunking the text content
- 🧬 Generating and storing sentence embeddings using Sentence Transformers
- 📦 Storing the embeddings and metadata in Weaviate
- 🔍 Performing semantic search on the stored embeddings

### 🖥️ Frontend – React
The React-based frontend allows users to:
- Enter a webpage URL
- Input a semantic search query
- View the top-k relevant results retrieved from the backend

---

## 📦 Requirements

Make sure you have the following installed:

- Python 3.8+
- FastAPI
- Weaviate (local or Docker)
- `sentence-transformers`
- `nltk`
- `requests`
- React 18+

> Install Python dependencies via:

```bash
pip install -r requirements.txt
```

## ⚙️ Setup Instructions

1. **Start Weaviate Locally**  
In the project root directory, a `docker-compose.yml` file is included to run Weaviate locally.

```bash
docker-compose up -d
```

2. **Run the Backend (FastAPI)**

Navigate into the backend directory and start the FastAPI server:

```bash
cd backend
uvicorn main:app --reload

```

3. **Run the Frontend (React)**

Navigate into the frontend directory, install dependencies, and start the development server:

```basb
cd frontend
npm install
npm run dev

```

