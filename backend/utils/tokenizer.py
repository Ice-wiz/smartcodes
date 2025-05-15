
from transformers import AutoTokenizer
from sentence_transformers import SentenceTransformer

from nltk.tokenize import sent_tokenize
from typing import List

# Load model and tokenizer
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = SentenceTransformer(MODEL_NAME)


def chunk_by_sentence(text: str, max_tokens: int = 500) -> List[str]:
    sentences = sent_tokenize(text)
    chunks = []
    current_chunk = ""
    current_len = 0

    for sentence in sentences:
        token_len = len(tokenizer.encode(sentence, add_special_tokens=False))
        if current_len + token_len <= max_tokens:
            current_chunk += " " + sentence
            current_len += token_len
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence
            current_len = token_len

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def embed_chunks(chunks: List[str]) -> List[List[float]]:
    return model.encode(chunks, convert_to_numpy=True).tolist()


def embed_query(query: str) -> List[float]:
    return model.encode([query], convert_to_numpy=True)[0].tolist()

