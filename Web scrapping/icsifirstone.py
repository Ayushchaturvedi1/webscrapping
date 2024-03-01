import requests
from pymongo import MongoClient
from bs4 import BeautifulSoup

client = MongoClient("mongodb+srv://doadmin:67K98DEUBAY0T214@lwai-mongo-c557243a.mongo.ondigitalocean.com/stale?authSource=admin&tls=true") 
mydatabase = client['stale']
mycollection = mydatabase.icsis

def icsi7():
    url = "https://www.icsi.edu/studymaterialnewsyllabus/"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    main_cell = soup.find(class_="TabbedPanelsContent")
    ul_cell = main_cell.find("ul")
    foundation_cell = ul_cell.find_all("li")  # first li
    foundation_cell1 = foundation_cell[:4]
    
    for particular in foundation_cell1:
        base_url = "https://www.icsi.edu"
        foundation_text = particular.get_text().strip()     # main text
        foundation_link = particular.find("a").get("href")
        
        if not foundation_link.startswith("htt"):
            foundation_link = base_url + foundation_link
        
        response1 = requests.get(foundation_link)
        soup1 = BeautifulSoup(response1.content, "html.parser")
        next_pg_foundation_ul = soup1.find(class_="TabbedPanelsContent")
        
        if next_pg_foundation_ul:
            next_pg_foundation_li = next_pg_foundation_ul.find_all("li")
            
        for each in next_pg_foundation_li:
            next_pg_foundation_a_tag = each.find_all("a")
            for one in next_pg_foundation_a_tag:
                next_pg_foundation_text = one.get_text().strip()
                next_pg_foundation_pdf_link = one.get("href")
                if not next_pg_foundation_pdf_link.startswith("htt"):
                    next_pg_foundation_pdf_link = base_url + next_pg_foundation_pdf_link
                    
                mycollection.insert_one({
                    "tagString": "ICSI <-> Studymaterialnewsyllabus <->"+foundation_text,
                    "metaData": {
                        "text": next_pg_foundation_text,
                        "pdfUrl": [next_pg_foundation_pdf_link]
                    }
                })

    foundation_last_cell = foundation_cell[4:]
    supplements_cell = foundation_last_cell[0].find("a")
    supplements_text = supplements_cell.get_text().strip()  # supplements text
    supplements_link = supplements_cell.get("href")  # supplements link

    response2 = requests.get(supplements_link)
    soup2 = BeautifulSoup(response2.content, "html.parser")
    first_div = soup2.find(class_="TabbedPanelsContent")
    first_ul = first_div.find("ul")
    all_li = first_ul.find_all("li")
    for part in all_li:
        next_pg_foundation_a = part.find("a")
        next_pg_foundation_a_link = next_pg_foundation_a.get("href")
        next_pg_foundation_a_text = next_pg_foundation_a.get_text().strip()  # getting each text of inner supplements
        response3 = requests.get(next_pg_foundation_a_link)
        soup3 = BeautifulSoup(response3.content, "html.parser")
        inner_supplements_pg = soup3.find(id="tabnavlist")
        inner_li = inner_supplements_pg.find_all("li")
        for part in inner_li:
            inner_a = part.find("a")
            if inner_a:
                inner_text = inner_a.get_text().strip()
                inner_pdf_link = inner_a.get("href")
                
                mycollection.insert_one({
                    "tagString": "ICSI <-> Studymaterialnewsyllabus <->"+ supplements_text,
                    "metaData": {
                        "text": next_pg_foundation_a_text + "<->" + inner_text,
                        "pdfUrl": [inner_pdf_link]
                    }
                })

# icsi7()


def icsi12():
    
        url = 'https://www.icsi.edu/student_pn/academic-portal/'
        base_url="https://www.icsi.edu"
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        cmss = soup.find_all(class_='description')
        for each in cmss:
            goto_link = each.find('a')
            main_goto_link = goto_link.get('href')
            if not main_goto_link.startswith('htt'):
                main_goto_link=base_url+ main_goto_link
            sub_r = requests.get(main_goto_link)
            sub_soup = BeautifulSoup(sub_r.content, 'html.parser')
            find_name = each.find_next('h2').get_text()
            title = sub_soup.find(class_='breadcrumb')
            all_span = title.find_all('span')
            main_title = all_span[-1].get_text()  # main title
            get_id = sub_soup.find(id='tabnavlist')
            if get_id:
                get_all_li = get_id.find_all('li')
            for one_li in get_all_li:
                pdf_text = one_li.find('a').get_text()
                pdf_link = one_li.find('a').get('href')
                mycollection.insert_one({'tagString':'ICSI <-> Company Secretaries Act,1980 and Rules & Regulation <->'+find_name,
                                         "metaData":{'text':pdf_text,'pdfUrl':[pdf_link]}})
        

# icsi12()


