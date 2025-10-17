from flask import Flask, request, jsonify
from utils.loader import extract_text_from_pdf, clean_text
from utils.chunking import chunk_text
from utils.embedding import embed_and_index
from utils.query import query_index
from utils.generator import generate_answer
import os
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get API key from .env
openai.api_key = os.getenv("OPENAI_API_KEY")
if not openai.api_key:
    raise ValueError("OPENAI_API_KEY is missing. Please set it in your .env file.")

app = Flask(__name__)

# Load and prepare data once at startup
pdf_path = os.getenv("PDF_PATH", "data/Leave Policy.pdf")
raw_text = extract_text_from_pdf(pdf_path)
cleaned_text = clean_text(raw_text)
chunks = chunk_text(cleaned_text)
index, embeddings, model = embed_and_index(chunks)

@app.route("/ask", methods=["POST"])
def ask_question():
    data = request.get_json()
    query = data.get("query")

    if not query:
        return jsonify({"error": "Query is required"}), 400

    # Retrieve relevant chunks
    retrieved_chunks = query_index(query, model, index, chunks)

    # Generate answer
    answer = generate_answer(query, retrieved_chunks)

    return jsonify({
        "query": query,
        "answer": answer,
        "context": retrieved_chunks
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)