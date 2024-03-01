import requests

url = "http://127.0.0.1:5000/get_document_content"  # Corrected route name
pdf_url = "https://labour.gov.in/sites/default/files/pib2000971.pdf"

data = {"url": pdf_url}

response = requests.post(url, json=data)

if response.ok:
    content = response.json()
    print(content)
else:
    print("Error:", response.text)
