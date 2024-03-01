from PyPDF2 import PdfReader
import requests
from io import BytesIO
from pymongo import MongoClient
import pandas as pd



def pdfcontent(name, url):
    client = MongoClient('localhost', 27017) 
    mydatabase = client['web_scrapping']
    mycollection = mydatabase.rbi 
    
    response = requests.get(url)
    if url.endswith(('.PDF','.pdf')):
        pdf_file = BytesIO(response.content)
        reader = PdfReader(pdf_file)
        # print(";;;;;")
        text = ''
        for page in reader.pages:
            text += page.extract_text()
        
        mycollection.insert_one({'PDF_name': name, 'PDF_text': text})
        
    elif url.endswith(('.xls', '.xlsx')):
        excel_file = BytesIO(response.content)
        # print(excel_file)
        reader = pd.read_excel(excel_file,header=0)
        # print(reader)
        
        # Drop columns with all NaN values
        reader = reader.dropna(axis=1, how='all')
        
        # Assuming 'reader' contains your DataFrame
        header_row = reader.iloc[0]  # Extract the header row
        # print(header_row)
        reader = reader[1:]  # Remove the first row containing the header information
        # Convert header row values to strings
        header_row = header_row.astype(str)
        reader.columns = header_row  # Set the header row as the column names
        # print(reader.columns)
    
        # Convert DataFrame to list of dictionaries
        excel_data = reader.to_dict(orient='records')
        
        # Insert JSON data into MongoDB
        mycollection.insert_one({'Excel_name': name, 'Excel_data': excel_data})

name = ""
url = "https://www.sebi.gov.in/sebi_data/attachdocs/1441362496725.pdf"

pdfcontent(name, url)