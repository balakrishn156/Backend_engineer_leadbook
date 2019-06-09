import requests
from bs4 import BeautifulSoup
import json 

url = 'https://www.sgmaritime.com/company-listings?page='
company_list = []
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
            company_dict = {}
            for link in content.find_all('h3'):
                web_url = 'https://www.sgmaritime.com'
                sub_link_url = web_url+link.a['href']
                company_dict['company_links'] = sub_link_url
                company_dict['company_name'] = link.a.text.decode().strip()                
                sub_page = requests.get(sub_link_url,verify=False)
                page_soup = BeautifulSoup(sub_page.content, 'html.parser')
                company_dict['company_address'] = page_soup.findAll("div",{"class":"col-md-7 company-contact"})[0].p.text.strip()
                company_dict['company_description'] = page_soup.findAll("div",{"class":"company-description"})[0].text
                company_phone = page_soup.findAll("div",{"class":"valuephone"})[0].a["href"].strip()
                company_dict['company_phone'] = company_phone[4:]
                #get company fax 
                company_fax = page_soup.findAll("div",{"class":"valuefax"})
                if company_fax == [] :
                    company_dict['company_fax'] = "None"
                else:
                    company_dict['company_fax'] = company_fax[0].a["href"].strip()[4:]
                #get company web address
                company_web = page_soup.findAll("div",{"id":"valuewebsite"})
                if company_web == [] :
                    company_dict['company_web']="None"
                else:
                    company_dict['company_web']=company_web[0].a["href"].strip()
                #get company map
                company_dict['company_map'] = page_soup.findAll("div",{"class":"col-md-5 company-map"})[0].iframe['src']
                #get company email
                company_email = page_soup.findAll("font",{"id":"companyEmail"})
                if company_email == [] :
                    company_dict['company_email'] = "None"
                else:
                    company_dict['company_email'] = company_email[0]["onclick"][17:40].split(",")[0]
                #get company product and services
                company_product = page_soup.findAll("div",{"class":"item"})
                if company_product == [] :
                    company_dict['company_product'] = "None"
                else:
                    productList = []
                    for content in company_product:
                        localDict = {}
                        localDict['product_type'] = content.a.img['alt']
                        localDict['product_url'] = web_url + content.a["href"].strip()
                        productList.append(localDict)
                    company_dict['company_product'] = productList
                #get company categories
                company_categories = page_soup.findAll("div",{"class":"company-description"})
                if company_categories == [] :
                    company_dict['company_categories'] = "None"
                else:
                    CategoryList = []
                    for content in company_categories[1].findAll('li'):
                        localDict = {}
                        localDict['parent_Category_name'] = content.a.text
                        localDict['parent_Category_url'] = web_url + content.a["href"].strip()
                        for child in content.findAll('a',{"class":"brand-child"}):
                            localDict['child_Category_name'] = child.text
                            localDict['child_Category_url'] = web_url + child["href"].strip()
                        CategoryList.append(localDict)
                    company_dict['company_categories'] = CategoryList
            company_list.append(company_dict)     
except:
    pass 

with open('company_profile.json','a') as write_file:
    json.dump(company_list,write_file)
    write_file.write("\n")