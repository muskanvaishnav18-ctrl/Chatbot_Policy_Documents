from .utils.loader import extract_text_from_pdf, clean_text
from .utils.chunking import chunk_text
from .utils.embedding import embed_and_index
from .utils.query import query_index
from .utils.generator  import generate_answer

pdf_path = "data/Leave Policy.pdf"

# Load and clean
raw_text = extract_text_from_pdf(pdf_path)
cleaned_text = clean_text(raw_text)

# Chunk
chunks = chunk_text(cleaned_text)

# Embed and index
index, embeddings, model = embed_and_index(chunks)

# Query
user_query = "What is the sick leave policy?"
retrieved_chunks = query_index(user_query, model, index, chunks)

# Generate answer
answer = generate_answer(user_query, retrieved_chunks)
print("Answer:", answer)