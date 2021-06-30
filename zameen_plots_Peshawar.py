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
    pagelink=requests.get(f'https://www.zameen.com/Plots/Peshawar-17-{i}.html')
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
        beds="None"
        area=all_data.find(class_='_1da99a35').find(class_='_7ac32433').find('span').text
        location=all_data.find(class_='_162e6469').text
        type="Plot"
        city="Peshawar"
        category="Selling"

        ads_list[count]=[image,tittle,price,area,location,type,city,category]
        count+=1

sql = '''INSERT INTO zameen_rental (image, title, price, bed, area, location, type, city, category) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'''
c.executemany(sql, ads_list.values())
conn.commit()
conn.close()

print(ads_list)

