import fitz
import re


pdf_path = "/home/LabsKraft/Chatbot_Policy_Documents/data/Leave Policy.pdf"
def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = ""
    for page in doc:
        text += page.get_text() + "\n"
    doc.close()
    return text
print(extract_text_from_pdf(pdf_path))

def clean_text(text):
    text = re.sub(r'\n+', ' ', text)
    text = re.sub(r'\r+', '', text)
    text = re.sub(r'[^a-zA-Z0-9\s.,;?!(){}-]', '', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'(Confidential|For Internal Use|Copyright)', '', text, flags=re.IGNORECASE)
    return text.strip()
