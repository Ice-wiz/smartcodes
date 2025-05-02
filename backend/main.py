

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

from utils.html_parser import clean_html
from utils.tokenizer import chunk_text
from utils.embedder import embed_chunks, embed_query
from utils.weaviate_client import weaviate_client


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    # or ["*"] for all origins (not recommended in production)
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],  # allow POST, GET, OPTIONS, etc.
    allow_headers=["*"],  # allow all headers including 'Content-Type'
)


class SearchInput(BaseModel):
    url: str
    query: str


@app.post("/search")
def search_chunks(input: SearchInput):
    try:
        response = requests.get(input.url, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        raise HTTPException(status_code=400, detail=str(e))

    # Step 1: Clean and chunk HTML
    cleaned_text = clean_html(response.text)
    chunks = chunk_text(cleaned_text)

    # Step 2: Embed the chunks
    chunk_vectors = embed_chunks(chunks)

    # Step 3: Insert into Weaviate
    for chunk, vector in zip(chunks, chunk_vectors):
        weaviate_client.insert_chunk_with_vector(chunk, input.url, vector)

    # Step 4: Embed the query
    query_vector = embed_query(input.query)

    # Step 5: Semantic search in Weaviate
    results = weaviate_client.search_by_vector(query_vector, limit=10)

    return {
        "query": input.query,
        "matches": results  # Each result includes chunk, url, and score
    }


# @app.post("/extract")
# def extract_text(input: QueryInput):
#     try:
#         response = requests.get(input.url, timeout=10)
#         response.raise_for_status()

#     except requests.RequestException as e:
#         raise HTTPException(status_code=400, detail=str(e))

#     cleaned_text = clean_html(response.text)
#     chunks = chunk_text(cleaned_text)

#     return {
#         "num_chunks": len(chunks),
#         "chunks": chunks[:10]
#     }
