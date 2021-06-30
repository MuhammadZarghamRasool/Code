from sqlite3 import dbapi2
import sqlite3
import pandas as pd
import requests
from bs4 import BeautifulSoup

count=0
ads_list={}
pagelink=requests.get('https://www.zameen.com/Rentals/Islamabad-3-1.html')
soup=BeautifulSoup(pagelink.content,'html.parser')
allAds=soup.findAll(class_='ef447dde')
# conn =sqlite3.connect("zameen_rental.db")
# c=conn.cursor()
# c.execute('''CREATE TABLE tests_rental(image VARCHAR, title TEXT, price INT, bed INT, area INT, Location TEXT)''')
         
for all_data in allAds:
    image=all_data.find('img').get('src')
    title=all_data.find('img').get('alt')
    price=all_data.find(class_='f343d9ce').text
    beds=all_data.findAll(class_='b6a29bc0')[0].text
    area=all_data.find(class_='_1da99a35').find(class_='_7ac32433').find('span').text
    location=all_data.find(class_='_162e6469').text
    ads_list[count]=[title,image,price,beds,area,location]
    count+=1
# sql = '''INSERT INTO tests_rental (image, title, price, bed, area, location) VALUES(?, ?, ?, ?, ?, ?)'''
# c.executemany(sql, ads_list.values())
# conn.commit()
# conn.close()
# if ads_list: 
#     df = pd.DataFrame.from_dict(ads_list,orient='index',columns=['title','image','price','beds','area','location'])
#     df.to_csv('rental.csv', mode='a',index=False,header=True)
print(ads_list)

