import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup

client = MongoClient("mongodb+srv://doadmin:67K98DEUBAY0T214@lwai-mongo-c557243a.mongo.ondigitalocean.com/stale?authSource=admin&tls=true") 
mydatabase = client['stale']
mycollection = mydatabase.rbifemas


def compounding1():                                                      #Type 2 -Compounding orders
    url = "https://rbi.org.in/scripts/Compoundingorders.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    tag_cell = soup.find(id="annual")
    main_tag = tag_cell.find(class_="page_title")
    tag = main_tag.get_text().strip()
    element_by_id = soup.find(class_="tablebg")
    rows = element_by_id.find_all("tr")
    
    rows = rows[1:]
    for row in rows:
        sr_cell = row.find("td")
        if sr_cell:
            applicant_cell = sr_cell.find_next("td")
            if applicant_cell:
                applicants = applicant_cell.get_text().strip()
            amount_cell = applicant_cell.find_next("td")
            if amount_cell:
                amount = amount_cell.get_text().strip()
            condition_cell = amount_cell.find_next("td")
            if condition_cell:
                condition = condition_cell.get_text().strip()
            link_cell = condition_cell.find_next("td")
            if link_cell:
                link_a = link_cell.find("a")
                link = link_a.get("href")
                            
            mycollection.insert_one({
                'tagString': "FEMA <->" + tag,
                "type2":{
                'text': applicants,
                'amount': amount,
                'amountPaid': condition,
                'pdfUrl': [link]
            }})

# compounding1()

#-----------------------------------------------------------------------------------------------------------------

def compounding2():                                #Type 2 -Compounding orders issued after/on March 1,2020
    url="https://rbi.org.in/scripts/SummaryCompoundingorders.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    tag_cell = soup.find(id="annual")
    main_tag = tag_cell.find(class_="page_title")
    tag = main_tag.get_text().strip()
    element_by_id = soup.find(class_="tablebg")
    rows = element_by_id.find_all("tr")
    
    rows = rows[1:]
    for row in rows:
        sr_cell = row.find("td")
        if sr_cell:
            name_cell = sr_cell.find_next("td")
            if name_cell:
                name = name_cell.get_text().strip()
            detail_cell = name_cell.find_next("td")
            if detail_cell:
                detail = detail_cell.get_text().strip()
            date_cell = detail_cell.find_next("td")
            if date_cell:
                date = date_cell.get_text().strip()
            amount_cell = date_cell.find_next("td")
            if amount_cell:
                amount = amount_cell.get_text().strip()
            
            mycollection.insert_one({
                'tagString': "FEMA <->" + tag,
                "type2":{
                'name': name,
                'text': detail,
                'date': date,
                'amount': amount
            }})
# compounding2()

#----------------------------------------------------------------------------------------------------------------

def lists():                                       #type 3  All are  stored in type3.json file
    url="https://rbi.org.in/Scripts/CategoryIILicencesCancelled.aspx"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    title_cell=soup.find(class_="page_title")
    # print(title_cell)
    title=title_cell.get_text().strip() # title of page
    table_cells=soup.find(class_="tablebg")
    tr_cells=table_cells.find_all("tr")
    first_tr_cell=tr_cells[0]
    first_tr=first_tr_cell.get_text().strip() #name of table
    # print(first_tr)  
    tr_cells=tr_cells[1:]
    for row in tr_cells:
        place_cells=row.find("a")
        place=place_cells.get_text().strip()
        # print(place)
        link=place_cells.get("href")
        mycollection.insert_one({"tagString":"FEMA <->"+first_tr,"type3":{"Place":place,"pdf_link":link}
        })  
            
# lists()

#-----------------------------------------------------------------------------------------------------------------

# def apdir():                                                                    #type 1 APDIR
#     url="https://rbi.org.in/Scripts/BS_ApCircularsDisplay.aspx"
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, "html.parser")
#     title_cell=soup.find(class_="page_title")
#     title1=title_cell.get_text().strip()
#     table_cell=soup.find(class_="tablebg")
#     tr_cell=table_cell.find_all("tr")
#     table_title=tr_cell[0].get_text().strip()
#     row_cell=tr_cell[2:]
#     for row in row_cell:
#         series_cell=row.find("td")
#         if series_cell:
#             series=series_cell.get_text().strip()
#             # print(series)
#         date_cell=series_cell.find_next("td")
#         # print(date_cell)
#         if date_cell:
#             date=date_cell.get_text().strip()
#             # print(date)
#         title_cell=date_cell.find_next("td")
#         if title_cell:
#             title=title_cell.get_text().strip()
#             title_l=title_cell.find("a")
#             if title_l:
#                 title_link=title_l.get("href")
#                 # print(title_link)
#                 if title_link.startswith("htt"):
#                     url1=title_link
#                     response1 = requests.get(url1)
#                     soup1 = BeautifulSoup(response1.content, "html.parser")
#                     next_pg_tablecell=soup1.find(class_="tablebg")
#                     next_pg_trcell=next_pg_tablecell.find("tr")
#                     next_pg_tr=next_pg_trcell.find("td")
#                     next_pg_td=next_pg_tr.find("a")
#                     next_pg_href=next_pg_td.get("href")
#                     title_dict={"title":title,"title_link":next_pg_href}
#                 else:
#                     title_link="https://rbi.org.in/Scripts/"+title_link
#                     url1=title_link
#                     response1 = requests.get(url1)
#                     soup1 = BeautifulSoup(response1.content, "html.parser")
#                     next_pg_tablecell=soup1.find(class_="tablebg")
#                     next_pg_trcell=next_pg_tablecell.find("tr")
#                     next_pg_tr=next_pg_trcell.find("td")
#                     next_pg_td=next_pg_tr.find("a")
#                     next_pg_href=next_pg_td.get("href")
#                     next_pg_headingtr=next_pg_trcell.find_next("tr")
#                     # print(next_pg_headingtr)
#                     next_pg_contenttr=next_pg_headingtr.find_next("tr")  
#                     next_pg_content=next_pg_contenttr.get_text().strip()
#                     # print(next_pg_content)
#                     title_dict={"title":title,"title_content":next_pg_content,"title_link":next_pg_href}
                    
                    
                    
#         pdf_cell=title_cell.find_next("td")
#         if pdf_cell:
#             pdf_l=pdf_cell.find("a")
#             if pdf_l:
#                 pdf_link=pdf_l.get("href")
            
#         mycollection.insert_one({"Tag" : "FEMA <->"+title1,'Type1':{"Table_title":table_title,"A.P.(Dir Series)":series,"Date":date,"Title":title_dict,"PDFs_link":pdf_link}})
                            
    
# # apdir()

#------------------------------------------------------------------------------------------------------------------

def Fema_Forms():                                              #type 2 FEMA Forms
    try:
        url = 'https://rbi.org.in/Scripts/BS_ViewFemaForms.aspx'
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        act = soup.find('table')
        rows = act.find_all('tr')[1:]
        # print(rows)
        for row in rows:
            # print(row)
            # for the fist column
            fema_form_text = row.find('td')
            main_fema_form_text = fema_form_text.get_text()
            if 'Click Here' in main_fema_form_text:
                main_fema_form_text = main_fema_form_text[:-10]
            # print(main_fema_form_text)

            # for the second column
            word_link_cell = fema_form_text.find_next('td')
            word_link = word_link_cell.select('a')
            main_word_link = ''  # removing this it arrays gets out of range
            if word_link:
                main_word_link = word_link[0].get('href')
            # print(main_word_link)

            # for column third
            pdf_link_cell = word_link_cell.find_next('td')
            pdf_link = pdf_link_cell.select('a')
            main_pdf_link = ''
            if pdf_link:
                main_pdf_link = pdf_link[0].get('href')
            # print(main_pdf_link)

            # insertion into DataBase
            mycollection.insert_one({"tagString" : "FEMA <-> Forms",'type2':{'text':main_fema_form_text,'wordUrl':[main_word_link],'pdfUrl':[main_pdf_link]}

            })
        # print('DONE')
    except Exception as e:
        print(e)

# Fema_Forms()