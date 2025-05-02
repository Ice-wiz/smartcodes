

from transformers import AutoTokenizer


MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)


def chunk_text(text: str, max_tokens: int = 500):
    paragraphs = text.split('\n')  # or use `nltk.sent_tokenize()` for better control

    chunks = []
    current_chunk = []
    current_tokens = 0

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        encoded = tokenizer.encode(para, add_special_tokens=False)
        if current_tokens + len(encoded) > max_tokens:
            # Add current chunk and start new one
            chunk_text = tokenizer.decode(tokenizer.encode(" ".join(current_chunk), add_special_tokens=False), skip_special_tokens=True)
            chunks.append(chunk_text)
            current_chunk = [para]
            current_tokens = len(encoded)
        else:
            current_chunk.append(para)
            current_tokens += len(encoded)

    # Add the last chunk
    if current_chunk:
        chunk_text = tokenizer.decode(tokenizer.encode(" ".join(current_chunk), add_special_tokens=False), skip_special_tokens=True)
        chunks.append(chunk_text)

    return chunks


# def chunk_text(text: str, max_tokens: int = 500):
#     tokens = tokenizer.encode(text, truncation=False)

#     chunks = []

#     for i in range(0, len(tokens), max_tokens):
#         chunks.append(tokens[i:i+max_tokens])

#     return [tokenizer.decode(chunk, skip_special_tokens=True) for chunk in chunks]
