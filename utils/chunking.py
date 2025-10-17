def chunk_text(text, chunk_size=500):
    paragraphs = text.split('\n\n')
    chunks = []
    current_chunk = ''
    
    for paragraph in paragraphs:
        if len(current_chunk + paragraph) > chunk_size:
            chunks.append(current_chunk)
            current_chunk = paragraph
        else:
            current_chunk += ' ' + paragraph
    
    if current_chunk:
        chunks.append(current_chunk)
    
    return chunks