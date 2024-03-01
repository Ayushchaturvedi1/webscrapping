import requests 
from bs4 import BeautifulSoup
from pymongo import MongoClient 

def web_scrap():
    try:
        client = MongoClient('localhost', 27017) 
        mydatabase = client['web_scrapping']
        mycollection = mydatabase.ibbi 
        
        url = "https://ibbi.gov.in/en/legal-framework/act"
        side = requests.get(url)
        sop = BeautifulSoup(side.content, "html.parser")
        frameworks = sop.find(class_='menu')
        for_links = frameworks.select('a')
        listing = []
        if for_links:
            for one in for_links:
                listing.append(one.get('href'))
        
        for link in listing:
            pagenumber = 1  # Reset pagenumber for each link
            while True:
                pages =  link+"?page="+str(pagenumber)
                r = requests.get(pages) 
                soup = BeautifulSoup(r.content, "html.parser")
                act = soup.find('table')
                rows = act.find_all('tr')
                
                for row in rows:
                    date_cell = row.find('td')
                    if date_cell:
                        date = date_cell.get_text().strip()
                        # Extracting subject
                        subject_cell = date_cell.find_next('td')
                        if subject_cell:
                            subject = subject_cell.get_text().strip()
                            links = []
                            for a_tag in row.find_all('a'):
                                onclick_value = a_tag.get('onclick')
                                if onclick_value:
                                    links.append(onclick_value.split("'")[1])
                            
                            if links:  # Ensure there are links before inserting into MongoDB
                                mycollection.insert_one({'date': date,'subject':subject ,'links': links[0]})
                
                disabled_next = soup.select('ul.pagination>li.next.disabled')
                if disabled_next:
                    break
                else:
                    pagenumber += 1
        print("DONE")
    except Exception as e:
        print(e)
        
web_scrap()
