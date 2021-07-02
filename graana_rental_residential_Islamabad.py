import requests
from bs4 import BeautifulSoup
# import sqlite3

# conn =sqlite3.connect("zameen_rental.db")
# c=conn.cursor()

count=0
ad_list={}
# j=90
# i=2670
# itr=0
# while j != 99:
link=requests.get("https://www.graana.com/residential/for_rent/islamabad/all/1?offset=2670&page=90")
#itr=str(link.status_code)
soup=BeautifulSoup(link.content,'html.parser')
all=soup.findAll(class_="row style_basic__19QWt")
    
    # print(i)
    # print(j)
    # # print(itr)
    # i=i+30
    # j=j+1

for all_data in all:
    image=all_data.find('img').get('src')
    title=all_data.find(class_="col-12 style_tileTitle__R0NOB").find('a').find('h2').text
    price=all_data.find(class_="style_priceTabView__pgFJO").find('strong').text
    #bed=all_data.find(class_="col-12 style_tileTitle__R0NOB").find(class_="gray small").find('span')
    bath=all_data.find(class_="col-12 style_tileTitle__R0NOB").find('p').text
    location=all_data.find(class_="col-12 style_tileTitle__R0NOB").find('p').text
    area=all_data.find(class_='col-4').text
    type="Residential"
    city="Islamabad"
    category="Rental"
    
    ad_list[count]=[image,title,price,bath,location,area,city,type,category]
    count+=1

# sql = '''INSERT INTO tests_rental (image, tittle, price, bed, area, location, type, city, category) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)'''
# c.executemany(sql, ad_list.values())
# conn.commit()
# conn.close()

  
print(ad_list)

