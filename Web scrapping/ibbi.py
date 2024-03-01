import requests,time
from bs4 import BeautifulSoup
from pymongo import MongoClient

def web_scrap():
    try:
        client = MongoClient('localhost', 27017) 
        mydatabase = client['web_scrapping']
        mycollection = mydatabase.ibbi 
        url = 'https://ibbi.gov.in/en/legal-framework/'
        r = requests.get(url)
        soup = BeautifulSoup(r.content,'html.parser')
        class_name = soup.find(id='block-mainnavigation-3')
        # print(class_name)
        find_li = class_name.find_all('a')
        print(find_li)
        list_of_links = []
        for i in find_li:
          all_href = i.get('href')
          if all_href:
           list_of_links.append(all_href)
        print(list_of_links)
        for i in list_of_links:
            pagenumber = 1
            while True:
                pages = "https://ibbi.gov.in"+i+"?page=" + str(pagenumber)
                # print(pages)
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
                            # print(len(links))
                            if links:  # Ensure there are links before inserting into MongoDB
                                mycollection.insert_one({'date': date,'subject':subject ,'links': links[0]})

                disabled_next = soup.select('ul.pagination>li.next.disabled')

                if disabled_next:
                    break
                else:
                    pagenumber += 1
        # time.sleep(5)
        print("DONE")
    except Exception as e:
        print(e)

web_scrap()
