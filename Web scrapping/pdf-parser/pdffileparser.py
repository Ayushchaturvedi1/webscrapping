from PyPDF2 import PdfReader
import requests
from io import BytesIO

def pdfcontent(url):
    response = requests.get(url)
    pdf_file = BytesIO(response.content)
    reader = PdfReader(pdf_file)
    pages_text = []  # Initialize an empty list to store text from each page
    for page in reader.pages:
        pages_text.append(page.extract_text())
    return pages_text

url = "https://rbi.org.in/upload/ERSystem/UM122012.pdf"
text_array = pdfcontent(url)
print(text_array)  # or do whatever you want with the extracted text
