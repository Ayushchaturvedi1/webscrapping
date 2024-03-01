from flask import Flask, request, jsonify
from PyPDF2 import PdfReader
from docx import Document
import pandas as pd
import requests
from io import BytesIO
from pymongo import MongoClient
import _thread


app = Flask(__name__)

def extract_text_from_pdf(url):
    try:
        response = requests.get(url)
        pdf_file = BytesIO(response.content)
        reader = PdfReader(pdf_file)
        pages_text = []
        for page in reader.pages:
            pages_text.append(page.extract_text())
        return pages_text
    except Exception as e:
        return str(e)

def extract_text_from_docx(url):
    try:
        response = requests.get(url)
        docx_content = response.content
        docx_file = BytesIO(docx_content)
        doc = Document(docx_file)
        full_text = []
        for paragraph in doc.paragraphs:
            full_text.append(paragraph.text)
        return '\n'.join(full_text)
    except Exception as e:
        return str(e)

def extract_data_from_excel(url):
    try:
        response = requests.get(url)
        excel_file = BytesIO(response.content)
        df = pd.read_excel(excel_file)
        excel_data = df.to_dict(orient='records')
        return excel_data
    except Exception as e:
        return str(e)

@app.route('/get_document_content', methods=['POST'])
def get_document_content():
    try:
        data = request.get_json()
        url = data['url']
        if url.endswith('.pdf'):
            content = extract_text_from_pdf(url)
        elif url.endswith('.docx'):
            content = extract_text_from_docx(url)
        elif url.endswith(('.xls', '.xlsx')):
            content = extract_data_from_excel(url)
        else:
            return jsonify({'error': 'Unsupported document format'})

        return jsonify({'content': content})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
