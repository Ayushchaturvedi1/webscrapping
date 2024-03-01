from flask import Flask, render_template, request
from io import BytesIO
from docx import Document
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    file = request.files['file']
    if file.filename.endswith(('.docx', '.doc')):
        text = extract_text_from_docx_file(file)
        return render_template('upload.html', extracted_text=text)
    else:
        return "Unsupported file format."

def extract_text_from_docx_file(file):
    docx_content = file.read()
    docx_file = BytesIO(docx_content)
    doc = Document(docx_file)
    full_text = []
    for paragraph in doc.paragraphs:
        full_text.append(paragraph.text)
    return '\n'.join(full_text)

if __name__ == '__main__':
    app.run(debug=True)
