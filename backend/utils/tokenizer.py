

from transformers import AutoTokenizer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def chunk_text(text: str, max_tokens: int = 500):
    tokens = tokenizer.encode(text, truncation=False)

    chunks = []

    for i in range(0, len(tokens), max_tokens):
        chunks.append(tokens[i:i+max_tokens])

    return [tokenizer.decode(chunk, skip_special_tokens=True) for chunk in chunks]
