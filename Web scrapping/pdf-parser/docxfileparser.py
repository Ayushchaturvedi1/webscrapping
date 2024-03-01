import requests
from io import BytesIO
from docx import Document

def extract_text_from_docx_url(docx_url):
    response = requests.get(docx_url)
    docx_content = response.content
    docx_file = BytesIO(docx_content)
    doc = Document(docx_file)
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)


docx_url = "https://dragon.pdf2go.com/download-file/bf10b575-5fa3-4663-9878-41070bde3487/385a33a3-90c0-4462-9f1b-8d2c9b68c9a0"  # Replace with your .docx file URL
text = extract_text_from_docx_url(docx_url)
print(text)
