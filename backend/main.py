from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

from utils.html_parser import clean_html
from utils.tokenizer import chunk_by_sentence, embed_chunks, embed_query
from utils.weaviate_client import weaviate_client


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # frontend origin
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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

    weaviate_client.reset_collection()

    from bs4 import BeautifulSoup
    soup = BeautifulSoup(response.text, "html.parser")

    # Remove unwanted tags (reuse same tags from your clean_html)
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav", "svg", "form", "input", "button", "aside"]):
        tag.decompose()
    for tag in soup.select('[style*="display:none"], [style*="visibility:hidden"], [hidden]'):
        tag.decompose()

    # Process paragraph-level blocks
    paragraph_tags = soup.find_all(["p", "div", "section", "article"])

    all_chunks = []
    all_vectors = []
    html_map = []

    for tag in paragraph_tags:
        raw_html = str(tag)
        clean_text = clean_html(raw_html)

        if not clean_text or len(clean_text.split()) < 5:
            continue  # Skip empty or tiny blocks

        sub_chunks = chunk_by_sentence(clean_text)

        if not sub_chunks:
            continue

        sub_vectors = embed_chunks(sub_chunks)

        all_chunks.extend(sub_chunks)
        all_vectors.extend(sub_vectors)
        # Map each chunk to the same HTML block
        html_map.extend([raw_html] * len(sub_chunks))

    # Insert into Weaviate
    for chunk, vector, html in zip(all_chunks, all_vectors, html_map):
        weaviate_client.insert_chunk_with_vector(
            chunk, input.url, vector, html)

    query_vector = embed_query(input.query)
    results = weaviate_client.search_by_vector(query_vector, limit=10)

    return {
        "query": input.query,
        "matches": results  # Includes chunk + html + score
    }


# Optional endpoint if you want to inspect chunks
# @app.post("/extract")
# def extract_chunks(input: SearchInput):
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
