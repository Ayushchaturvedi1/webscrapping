import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup


client = MongoClient("mongodb+srv://doadmin:67K98DEUBAY0T214@lwai-mongo-c557243a.mongo.ondigitalocean.com/stale?authSource=admin&tls=true") 
mydatabase = client['stale']
mycollection = mydatabase.fcras

def fcra2nd():
    url="https://fcraonline.nic.in/Home/order.aspx"
    response=requests.get(url, verify=False)
    soup=BeautifulSoup(response.content,"html.parser")
    div_main=soup.find(id="Div_Contact_order")
    h4_main=div_main.find("h4").get_text().strip()           #mainheading
    # print(h4_main)
    div_next=div_main.find(class_="form_inner_box")
    ul_main=div_next.find_all("ul")
    # print(ul_main)
    for each in ul_main:
        li_cell=each.find_all("li")
        # print(li_cell)
        for one in li_cell:
            a_cell=one.find("a")
            # print(a_cell)
            if a_cell:
                text_each=a_cell.get_text().strip()
            # print(text_each)
                link_cell=a_cell.get("href")
            # print(link_cell)
            if not link_cell.startswith("htt"):
                link_cell="https://fcraonline.nic.in/Home/"+ link_cell
            if link_cell.endswith(".pdf") or link_cell.endswith(".PDF"):
                pdf_link = link_cell
                excel_link= None
                # print(link_cell)

            else:
                excel_link=link_cell
                pdf_link=None
                # print(excel_link)
        
            mycollection.insert_one({"tagString": "FCRA <-> "+h4_main,
                                    "metaData":{
                                        "text":text_each,
                                        "pdfURL":[pdf_link],
                                        "excelURL":[excel_link]
                                    }})
fcra2nd()