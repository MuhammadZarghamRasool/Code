import sqlite3
import requests
from bs4 import BeautifulSoup

conn =sqlite3.connect("zameen_rental.db")
c=conn.cursor()

count=0
ads_list={}
i=0
itr=0

while itr != "404":
    pagelink=requests.get(f'https://www.zameen.com/Homes/Islamabad-3-{i}.html')
    itr=str(pagelink.status_code)
    print(i)
    print(itr)
    soup=BeautifulSoup(pagelink.content,'html.parser')
    allAds=soup.findAll(class_='ef447dde')
    i=i+1
 
    for all_data in allAds:
        image=all_data.find('img').get('src')
        tittle=all_data.find('img').get('alt')
        price=all_data.find(class_='f343d9ce').text
        beds=all_data.findAll(class_='b6a29bc0')[0].text
        area=all_data.find(class_='_1da99a35').find(class_='_7ac32433').find('span').text
        location=all_data.find(class_='_162e6469').text
        type="Residential"
        city="Islamabad"
        category="Selling"

        ads_list[count]=[tittle,image,price,beds,area,location,type,city,category]
        count+=1
    
print(ads_list)

