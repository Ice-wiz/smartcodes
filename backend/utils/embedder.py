

from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def embed_chunks(chunks: list[str]) -> list[list[float]]:
    return model.encode(chunks, convert_to_numpy=True).tolist()

def embed_query(query: str) -> list[float]:
    return model.encode([query], convert_to_numpy=True)[0].tolist()


