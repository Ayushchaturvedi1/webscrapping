import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup
import time
import re

client = MongoClient("mongodb+srv://doadmin:67K98DEUBAY0T214@lwai-mongo-c557243a.mongo.ondigitalocean.com/stale?authSource=admin&tls=true") 
mydatabase = client['stale']
mycollection = mydatabase.mlaes

def media():
    pages = 0
    while pages <= 19:  # Adjust the condition to stop at page 20
        url = "https://labour.gov.in/pib-news?title=&page=" + str(pages)
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        main_div = soup.find(class_="views-table cols-4")
        body_cell = main_div.find("tbody")
        tr_cell = body_cell.find_all("tr")
        for each in tr_cell:
            first_td = each.find("td")
            second_td = first_td.find_next("td")               
            second_element = second_td.get_text().strip()  # Second column
            third_td = second_td.find_next("td")
            third_element = third_td.get_text().strip()
            fourth_td = third_td.find_next("td")
            a_cell = fourth_td.find("a")
            if a_cell:
                pdfurl = a_cell.get('href')
            # print(pdfurl)
            mycollection.insert_one({"tagString":"Ministry of Labour and Employement <-> Press Releases",
            "metaData":{
                "text": second_element,
                "pdfUrl": [pdfurl]
                
            }})
                
        pages += 1
        # time.sleep(2)

media()

def document1():
    url1="https://labour.gov.in/social-security-agreement"
    response1=requests.get(url1)
    soup1=BeautifulSoup(response1.content,"html.parser")
    first_div=soup1.find(class_="aboutRightContainer")
    # print(main_text)
    innerdiv1=first_div.find(class_="field-content")
    # print(innerdiv1)
    body1=innerdiv1.find("tbody")
    # print(body1)
    tr_cell1=body1.find_all("tr")
    tr_cell1=tr_cell1[1:]
    # print(tr_cell1)
    for each in tr_cell1:
        first_td1=each.find("td")
        second_td1=first_td1.find_next("td")
        second_element1=second_td1.get_text().strip()
        third_td1=second_td1.find_next("td")
        a_1=third_td1.find("a").get("href").strip()
        # print(a_1)
        mycollection.insert_one({"tagString ": "Ministry of Labour and Employement <-> Social Security Agreement",
                                 "metaData":{
                                    "text": second_element1,
                                    "pdfUrl": [a_1]
                                 }})
    
    url2="https://labour.gov.in/monthly-progress-report"
    response2=requests.get(url2)
    soup2=BeautifulSoup(response2.content,"html.parser")
    main_div=soup2.find("table")
    # print(main_div)
    tr_cell2=main_div.find_all("tr")
    # print(tr_cell2)
    tr_cell2=tr_cell2[1:]
    for one in tr_cell2:
        first_td2=one.find("td")
        # print(first_td2)
        first_element2=first_td2.get_text().strip()
        second_td2=first_td2.find_next("td")
        a_2=second_td2.find("a").get("href").strip()
        # print(first_element2)
        # print(a_2)
        mycollection.insert_one({"tagString ": "Ministry of Labour and Employement <-> Monthly Progress Report",
                                 "metaData":{
                                    "text": first_element2,
                                    "pdfUrl": [a_2]
                                 }})
        
    
    url3="https://labour.gov.in/annual-reports"
    response3=requests.get(url3)
    soup3=BeautifulSoup(response3.content,"html.parser")
    tbody3=soup3.find("tbody")
    # print(tbody3)
    tr_cell3=tbody3.find_all("tr")
    # print(tr_cell3)
    for part in tr_cell3:
        first_td3=part.find("td")
        second_td3=first_td3.find_next("td")
        second_element3=second_td3.get_text().strip()
        second_element3=re.sub(r'\s*\([^)]*\)\s*', '', second_element3)  
        # print(second_element3)
        third_td3=second_td3.find_next("td")
        a_3=third_td3.find("a").get("href").strip()
        # print(a_3)
        mycollection.insert_one({"tagString ": "Ministry of Labour and Employement <-> Annual Report",
                                 "metaData":{
                                    "text": second_element3,
                                    "pdfUrl": [a_3]
                                 }})
    
    
    url4="https://labour.gov.in/annual-reports-autonomous-bodies"
    response4=requests.get(url4)
    soup4=BeautifulSoup(response4.content,"html.parser")
    tbody4=soup4.find("tbody")
    # print(tbody4)
    tr_cell4=tbody4.find_all("tr")
    for ek in tr_cell4:
        first_td4=ek.find("td")
        second_td4=first_td4.find_next("td")
        second_element4=second_td4.get_text().strip()
        third_td4=second_td4.find_next("td")
        third_element4=third_td4.get_text().strip()
        fourth_td4=third_td4.find_next("td")
        a_4=fourth_td4.find("a").get("href").strip()
        # print(a_4)
        mycollection.insert_one({"tagString ": "Ministry of Labour and Employement <-> Annual Reports for Autonomous Bodies",
                                 "metaData":{
                                    "text": second_element4,
                                    "pdfUrl": [a_4]
                                 }})
        
        
    
    
    
document1()
