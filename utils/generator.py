import openai

def generate_answer(query, retrieved_chunks):
    context = "\n".join(retrieved_chunks)
    prompt = f"""
    You are an assistant that answers questions based on company policy documents.
    Context:
    {context}
    Question: {query}
    Answer:
    """
    openai.api_key = "OPENAI_API_KEY"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful assistant for internal policy queries."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
        max_tokens=500
    )
    return response['choices'][0]['message']['content']