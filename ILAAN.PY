import pandas as pd
import requests
from bs4 import BeautifulSoup

# count=0
# ads_list={}
# i=0
# itr=0
# while itr != "404":
pagelink=requests.get('https://www.ilaan.com/property-for-sale?q=islamabad&pgno=1')

# itr=str(pagelink.status_code)
# print(i)
# print(itr)
soup=BeautifulSoup(pagelink.content,'html.parser')
allAds=soup.find(class_="premium-list property-list property-box-5 shade show-cls")
#print(allAds)
#     i=i+1
 
    # for all_data in allAds:
    # image=all_data.find('img').get('src')
#tittle=allAds.find('img').get('alt')
price=allAds.find(class_='col-md-8 col-sm-8 col-8 heading-div').find(class_='tittle').find('a').text
    #     beds=all_data.findAll(class_='b6a29bc0')[0].text
    #     area=all_data.find(class_='_1da99a35').find(class_='_7ac32433').find('span').text
    #     location=all_data.find(class_='_162e6469').text
    #     ads_list[count]=[image,tittle,price,beds,area,location]
    #     count+=1
print(price)
# df = pd.DataFrame.from_dict(ads_list,orient='index',columns=['image','tittle','price','beds','area','location'])
# df.to_csv('rental.csv', mode='a',index=False,header=True)
    
# print(ads_list)

 