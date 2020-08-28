import time
import traceback
import schedule as schedule
import django
import requests
import json
import pandas as pd
import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'Best_Buy.settings'
django.setup()
from App_Best_Buy.models import Category,Best_Buy
allData = []
# list = pd.DataFrame(columns=['ModelNumber', 'Name', 'SKU', 'ImageURL', 'SalePrize', 'RegularPrize','ProductURL'])
dic={}

def save_data(product_list,category):
    try:
        query_obj = Category.objects.filter(category_name=category)
        # print(query_obj.exists())
        if query_obj.exists() == True:
            query_obj = query_obj[0]
            # print(query_obj)
            print('category already exists')
        else:
            query_obj = Category(category_name=category)
            # print(query_obj)
            query_obj.save()
            print('category save')
        bestbuy_obj = Best_Buy.objects.filter(product_link=product_list['ProductURL']).first()
        if bestbuy_obj == None:
            print("new object")
            getid = query_obj.id
            best_buy_save = Best_Buy(
                category=Category(str(getid)),
                model_number=str(product_list['ModelNumber']),
                name=str(product_list['Name']),
                sku=str(product_list['SKU']),
                image=str(product_list['ImageURL']),
                sale_price=str(product_list['SalePrize']),
                regular_price=str(product_list['RegularPrize']),
                product_link=str(product_list['ProductURL'])

            )
            best_buy_save.save()
            print("save")
    except Exception as e:
        print(e.__str__())
        traceback.print_exc()

def getData(id):
    newId = str(id)
    URL = "https://api.bestbuy.com/v1/products((categoryPath.id=" + newId + "))?apiKey=zuKN5cDvqHGmtnzEm86cff3f&sort=modelNumber.asc&show=modelNumber,name,salePrice,regularPrice,sku,image,mobileUrl&pageSize=30&format=json"
    r = requests.get(url=URL)
    data = r.json()
    prod = data["products"]
    totalPages = data['totalPages']
    i = 1
    while i < totalPages:
        newPage = str(i)
        print("page num: ", newPage)
        URL = "https://api.bestbuy.com/v1/products((categoryPath.id=" + newId + "))?apiKey=zuKN5cDvqHGmtnzEm86cff3f&sort=modelNumber.asc&show=modelNumber,name,salePrice,regularPrice,sku,image,mobileUrl&pageSize=30&page=" + newPage + "&format=json"
        r = requests.get(url=URL)
        data = r.json()
        prod = data["products"]
        allData.append(prod)
        num = len(prod)
        n = 0
        while n < num:
            currentDict = prod[n]
            ModelNumber = currentDict["modelNumber"]
            Name = currentDict["name"]
            SKU = currentDict["sku"]
            ImageURL = currentDict["image"]
            SalePrize = currentDict["salePrice"]
            RegularPrize = currentDict["regularPrice"]
            ProductURL = currentDict["mobileUrl"]

            # list.loc[len(list)] =[ModelNumber, Name, SKU, ImageURL, SalePrize, RegularPrize, ProductURL]
            # print(list)
            data={
                "ModelNumber":ModelNumber,
                "Name":Name,
                "SKU":SKU,
                "ImageURL":ImageURL,
                "SalePrize":SalePrize,
                "RegularPrize":RegularPrize,
                "ProductURL":ProductURL
            }
            save_data(data,newId)
            n += 1

        i += 1


if __name__ == '__main__':

    categories = ['pcmcat209400050001', 'abcat0501000', 'abcat0401000', 'pcmcat242800050021', 'abcat0204000',
                  'pcmcat241600050001',
                  'pcmcat254000050002', 'pcmcat209000050006', 'abcat0502000', 'pcmcat232900050000', 'pcmcat295700050012',
                  'pcmcat310200050004',
                  'pcmcat243400050029', 'abcat0904000', 'abcat0901000', 'abcat0912000', 'abcat0101000', 'abcat0910000',
                  'pcmcat273800050036',
                  'pcmcat300300050002']




    def cat(categories):
        for cat in categories:
            getData(cat)
            print('length: ', len(allData))

    while True:
        schedule.every(1).hour.do(cat(categories))
        schedule.run_pending()
        time.sleep(1)
