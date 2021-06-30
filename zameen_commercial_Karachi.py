import requests
from bs4 import BeautifulSoup
import sqlite3

conn =sqlite3.connect("zameen_rental.db")
c=conn.cursor()

count=0
ads_list={}
i=35
itr=0
while itr != "404":
    pagelink=requests.get(f'https://www.zameen.com/Commercial/Karachi-2-{i}.html')
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
        type="Commercial"
        city="Karachi"
        category="Selling"
        
        ads_list[count]=[image,tittle,price,beds,area,location,type,city,category]
        count+=1
sql = '''INSERT INTO tests_rental (image, tittle, price, bed, area, location, type, city, category) VALUES(?,?, ?, ?, ?, ?, ?, ?, ?)'''
c.executemany(sql, ads_list.values())
conn.commit()
conn.close()
#Storing data in CSV form 
# df = pd.DataFrame.from_dict(ads_list,orient='index',columns=['image','tittle','price','beds','area','location'])
# df.to_csv('rental.csv', mode='a',index=False,header=True)
    
print(ads_list)

 