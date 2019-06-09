import requests
from bs4 import BeautifulSoup
import json 

url = 'https://www.sgmaritime.com/company-listings?page='
list = []
try:
    for x in range(1,600):
        page_url= url+'/'+str(x)
        page = requests.get(page_url,verify=False)  
        # print(page.status_code)
        # print(page.content)
        soup = BeautifulSoup(page.content, 'html.parser')
        # print(soup.prettify())
        contents = soup.find_all('div', class_='col-md-9 col-xs-8 company-details')
        for content in contents:
            for link in content.find_all('h3'):
                dict = {}
                link_url = 'https://www.sgmaritime.com'
                dict['company_links'] = link_url+link.a['href']
                dict['company_name'] = link.a.text.decode().strip()
                dict['country'] = "Singapore"
                list.append(dict)         
except:
    pass 

with open('company_index.json','a') as write_file:
    json.dump(list,write_file)
    write_file.write("\n")