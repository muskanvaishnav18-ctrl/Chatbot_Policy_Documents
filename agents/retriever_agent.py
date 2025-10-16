import fitz  # PyMuPDF for PDF extraction
import re
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

# Function to extract text from a PDF file
def extract_text_from_pdf(pdf_path):
    # Open the PDF file
    doc = fitz.open("/home/LabsKraft/Chatbot_Policy_Documents/data/Leave Policy.pdf.txt")
    text = ""
    
    # Extract text from each page
    for page_num in range(doc.page_count):
        page = doc.load_page(page_num)  # Load each page
        text += page.get_text()  # Extract text from the page
    
    return text

# Function to clean the extracted text
def clean_text(text):
    # Remove extra newlines or carriage returns
    text = re.sub(r'\n+', ' ', text)  # Replace multiple newlines with a single space
    text = re.sub(r'\r+', '', text)   # Remove carriage returns
    
    # Remove special characters (keep only alphanumeric and spaces)
    text = re.sub(r'[^a-zA-Z0-9\s.,;?!(){}-]', '', text)  # Keep basic punctuation
    
    # Remove multiple spaces
    text = re.sub(r'\s+', ' ', text)  # Replace multiple spaces with a single space
    
    # Remove irrelevant sections (e.g., disclaimers, headers)
    text = re.sub(r'(Confidential|For Internal Use|Copyright)', '', text, flags=re.IGNORECASE)
    
    # Clean up any unnecessary characters
    text = text.strip()  # Remove leading and trailing spaces
    
    return text

# Function to chunk the cleaned text
def chunk_text(text, chunk_size=500):
    paragraphs = text.split('\n\n')  # Split text by paragraphs (two newlines)
    
    chunks = []
    current_chunk = ''
    
    # Process each paragraph and create chunks
    for paragraph in paragraphs:
        if len(current_chunk + paragraph) > chunk_size:
            # If the chunk exceeds the desired size, start a new chunk
            chunks.append(current_chunk)
            current_chunk = paragraph
        else:
            # Otherwise, continue appending to the current chunk
            current_chunk += ' ' + paragraph
            
    # Add the last chunk
    if current_chunk:
        chunks.append(current_chunk)
        
    return chunks

# Function to create embeddings and index them using FAISS
def embed_and_index(chunks):
    # Load Sentence-BERT model
    model = SentenceTransformer('all-MiniLM-L6-v2')

    # Convert each chunk into an embedding
    embeddings = model.encode(chunks)
    
    # Initialize FAISS index
    dimension = embeddings.shape[1]  # Dimensionality of the embeddings
    index = faiss.IndexFlatL2(dimension)  # Using L2 distance for similarity search
    
    # Add embeddings to the index
    index.add(np.array(embeddings))
    
    # Save the index for later use (optional)
    faiss.write_index(index, "policy_embeddings.index")
    
    return index, embeddings

# Function to query the index
def query_index(query, model, index, chunks, top_k=3):
    # Create the query embedding
    query_embedding = model.encode([query])
    
    # Search for the top_k most relevant chunks
    D, I = index.search(np.array(query_embedding))
