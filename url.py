print("========== Start ==========")
import time
from datetime import datetime
print(time.ctime())
st = time.time()
import urllib.request
import pandas as pd
import os
import re
import requests
from urllib.request import Request, urlopen

currentDirectory = os.getcwd()

Main_url = "https://www.ahuzot.co.il/Parking/All/"
parking_url = 'https://www.ahuzot.co.il/Parking/ParkingDetails/?ID='


fp = urllib.request.urlopen(Main_url)
mybytes = fp.read()
Mainstr = mybytes.decode("utf8")
fp.close()


urllist = []

for i in range(0,200):
    url = parking_url + "{}".format(i) + '"><img'
    if url in Mainstr:
        urllist.append(parking_url + "{}".format(i))
        
print("url field is ready")

IDlist = []       
for i in urllist:
    n = int(re.findall("\d+", i)[0])
    IDlist.append(n)
    
print("ID field is ready")
    
nameslist = []    
Xlocatios = []
Ylocatios = []
Addresslist  =[]
disabledlist  =[]
Amountparkinglist = []
Activitytimelist = []
pricelist = []

for ind in range(0,len(urllist)):
#for ind in range(0,91):         
    fp = urllib.request.urlopen(urllist[ind])
    mybytes = fp.read()
    urlstr = mybytes.decode("utf8")
    fp.close()
    locationstr = urlstr[urlstr.find("&c1"):urlstr.find("&c1")+ 50]
    location_y = locationstr[locationstr.find("c1=3") + 3 : locationstr.find("&c2=3")]
    location_x = locationstr[locationstr.find("c2=3") + 3: locationstr.find("\'")]
    Xlocatios.append(location_x)
    Ylocatios.append(location_y)
    addressstr = urlstr[urlstr.find("כתובת החניון"):urlstr.find("כתובת החניון")+ 100]
    Address = addressstr[addressstr.find("p;<b>") +5 :addressstr.find("</b></span>")]
    Addresslist.append(Address)
    Activitytimestr = urlstr[urlstr.find("שעות פעילות החניון"):urlstr.find("שעות פעילות החניון")+ 150]
    Activitytime = Activitytimestr[Activitytimestr.find("p;<b>") +5 :Activitytimestr.find("</b></span>")]
    Activitytimelist.append(Activitytime)
    pricestr = urlstr[urlstr.find("תעריף החניון"):urlstr.find("תעריף החניון")+ 200]
    price = pricestr[pricestr.find("<b>") +5 :pricestr.find("</b></span>")]
    pricelist.append(price)
    namestr = urlstr[urlstr.find("חניון "):urlstr.find("חניון ")+ 50]
    name = namestr[namestr.find("חניון ") :namestr.find("</s")]
    nameslist.append(name)
    disabledstr = urlstr[urlstr.find("החניון מונגש"):urlstr.find("החניון מונגש")+ 50]
    disabled = disabledstr[disabledstr.find("החניון") :disabledstr.find("</b>")]
    disabledlist.append(disabled)
    Amountparkingstr = urlstr[urlstr.find("מקומות חנייה בחניון"):urlstr.find("מקומות חנייה בחניון")+ 50]
    Amountparking = Amountparkingstr[Amountparkingstr.find(":") + 1 :Amountparkingstr.find("<")]
    Amountparkinglist.append(int(Amountparking))


print("name field is ready")
print("Address field is ready")
print("disabled field is ready")
print("Amountparking field is ready")
print("ctivitytime field is ready")

pricelistfix = []
for price in pricelist:
    for letter in price:
        if not (1488 <= ord(letter) <= 1514 or 57 >= ord(letter) >= 48 or letter == "-" or letter == " " or letter == "₪") :
            price = price.replace(letter,"")
    pricelistfix.append(price)

print("price field is ready")

from urllib import request
from urllib.request import Request, urlopen

X2039 = []
y2039 = []
for x in range(0,len(Xlocatios)):
    if "3" in Xlocatios[x]: 
        url = 'http://epsg.io/trans?x={}&y={}&z=0&s_srs=4326&t_srs=2039&callback=jsonpFunction'.format(Xlocatios[x],Ylocatios[x])
        request_site = Request(url, headers={"User-Agent": "Mozilla/5.0"})
        webpage = urlopen(request_site).read()
        webpage = str(webpage)
        outputx = float(webpage[webpage.find('"x": "') + 6: webpage.find('", "y"')])
        outputy = float(webpage[webpage.find('"y": "') + 6: webpage.find('", "z"')])    
        X2039.append(outputx)
        y2039.append(outputy)
    else:
        X2039.append(None)
        y2039.append(None)
 
print("X field is ready")
print("Y field is ready")                
  
columns = ["ID","URL","Name","X","Y","Address","disabled","Amountparking","Activitytime","price"]

# Converting to excel
df = pd.DataFrame(list(zip(IDlist,urllist,nameslist,X2039,y2039,Addresslist,disabledlist,Amountparkinglist,Activitytimelist,pricelistfix)), columns = columns)

df.to_excel(r"{}\Output.xlsx".format(currentDirectory))

print("Output.xlsx is ready")    
 
print("========== End ==========")
et = time.time()
res = et - st
final_res = str(res / 60)
print("Done!")
print("\N{smiling face with sunglasses}")
print(time.ctime())
print('Execution time:', final_res[0:final_res.find(".") + 3], 'minutes')







    
    


    
    
    



   

    