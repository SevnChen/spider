# -*- coding: utf-8 -*-
#!/usr/bin/env python
# @Time    : 2016/10/28 15:16
# @Author  : SevnChen
# @Site    : 
# @File    : spider.py
# @Software: PyCharm

import pandas as pd
from bs4 import BeautifulSoup
import json
#import chardet
from getobj import GetObj
from db import ConnectDB


def Getcarurl(url):
    obj = GetObj(url)
    html=obj.gethtml()
    coding=obj.getcodeing(html)
    soup=BeautifulSoup(html,'html5lib',from_encoding=coding)
    #print soup.original_encoding
    box_all=soup.find_all("table", attrs = {"class":["carList"]})
    content_link = []
    for box in box_all:
        soup_link=BeautifulSoup(str(box),"html5lib")
        box_li = soup_link.find_all("li")
        for item in box_li:
            tmp=BeautifulSoup(str(item), "html5lib")
            for link in tmp.find_all('a'):
                content_link.append("http://db.auto.sohu.com" + link.get('href'))
    return content_link

def Save_data(manufacturer, brand, series, model_id_dict, thead_list1, table_dict1, thead_list2, table_dict2, url_car):
    #print manufacturer, brand, series,model_id_dict["id"]
    #表1处理
    table1_head_json = eval("u'"+(json.dumps(thead_list1))+"'")
    table1_content_json = json.dumps(table_dict1)
    table1_content_json = eval("u'"+(table1_content_json.replace("\u25cf", "1").replace("-", "0").replace("null", "0"))+"'")
    #表2处理
    table2_head_json = eval("u'"+(json.dumps(thead_list2))+"'")
    table2_content_json = json.dumps(table_dict2)
    table2_content_json = eval("u'"+(table2_content_json.replace("\u25cf", "1").replace("-", "0").replace("null", "0"))+"'")
    db=ConnectDB()
    db.insert(table_name= "car_maintenance", 
              manufacturer =manufacturer,
              brand =brand,
              series =series,
              car_id_souhu = model_id_dict["id"] ,
              name =eval("u'"+(model_id_dict["name"])+"'"),
              year =model_id_dict["year"],
              table1_head = table1_head_json,
              table1_content =table1_content_json,
              table2_head = table2_head_json,
              table2_content =table2_content_json,
              url_car = url_car)
    db.dbclose()
    
def GetMaintenance(url_maintenance,num_car_model, num_url_car):
    obj = GetObj(url_maintenance)
    html=obj.gethtml()
    soup_all=BeautifulSoup(html, "html5lib", from_encoding = 'utf-8')
    #获取厂商-品牌-车系数据
    content_head = soup_all.find_all("span", attrs = {"class":["daohang"]})
    flag = len(BeautifulSoup(str(content_head), "html5lib", from_encoding = 'utf-8').find_all("a"))
    if flag != 5:
        return url_maintenance
    elif flag == 5:
        if len(content_head) == 1:
            soup_head = BeautifulSoup(str(content_head).encode("utf-8"), "html5lib", from_encoding = 'utf-8')
            brand = eval("u'"+(str(soup_head.find_all("a")[2].string))+"'")
            manufacturer = eval("u'"+str((soup_head.find_all("a")[3].string))+"'")
            series = eval("u'"+str((soup_head.find_all("a")[4].string))+"'")
        #获取该车系下的所有车型和年限以及对应ID
        box_model = soup_all.find_all("div", attrs = {"id":["modelid"]})
        soup_model = BeautifulSoup(str(box_model) ,"html5lib", from_encoding = 'utf-8')
        model_id_dict = {}
        for item in soup_model.find_all("li"):
            model_id_dict[item.get("id")] = {"id": item.get("id"), "year":item.get("data-year"), "name":item.string}
        #maintenance_dict = {}
        #获取每个车型的保养配置
        num_car = len(model_id_dict)
        num_car_tmp = 0
        for id in model_id_dict:
            id_tmp = id + "_L"
            #获取具体保养配置
            #第1层：找到整体配置
            box_model_Maintenance = soup_all.find("div", attrs = {"id":[id_tmp]})
            soup_Maintenance = BeautifulSoup(str(box_model_Maintenance), "html5lib", from_encoding = 'utf-8')
            #第2-1层，找到表1
            box_mm_tabel1 = soup_Maintenance.find("table",  attrs = {"class":["tabel1"]})
            soup_mm_tabel1 = BeautifulSoup(str(box_mm_tabel1), "html5lib", from_encoding = 'utf-8')
            #第2-2层，找到表1的头
            box_mm_tabel1_thead = soup_mm_tabel1.find_all("th")
            thead_list1 = []
            for item in box_mm_tabel1_thead:
                tmp = ""
                for i in item.stripped_strings:
                    tmp += i
                thead_list1.append(tmp)
            #第3-2层，找到表1的行头
            #box_mm_tabel1_tbody_1 = soup_mm_tabel1.find_all("td", attrs = {"class":["bg"]})
            #bg_list1 = []
            #for item in box_mm_tabel1_tbody_1:
            #    bg_list1.append(item.string)
            #第2-3层，找到表1的内容  
            table_dict1 = {}
            box_mm_tabel1_tbody_2 = soup_mm_tabel1.find_all("td")
            column_num = len(thead_list1)
            if len(box_mm_tabel1_tbody_2)%column_num == 0:
                tmp = ""
                tmp_list = []
                for i in range(len(box_mm_tabel1_tbody_2)):
                    if i%column_num == 0:
                        tmp_list = []
                        tmp = box_mm_tabel1_tbody_2[i].string
                    else:
                        tmp_list.append(box_mm_tabel1_tbody_2[i].string)
                    if i%column_num == column_num - 1:
                        table_dict1[tmp] = tmp_list
            #第3-1层，找到表2
            box_mm_tabel2 = soup_Maintenance.find("table",  attrs = {"class":["tabel2", "t10"]})
            soup_mm_tabel2 = BeautifulSoup(str(box_mm_tabel2), "html5lib", from_encoding = 'utf-8')
            #第3-2层，找到表2的表头
            box_mm_tabel2_thead = soup_mm_tabel2.find_all("th")
            thead_list2 = []
            for item in box_mm_tabel2_thead:
                tmp = ""
                for i in item.stripped_strings:
                    tmp += i
                thead_list2.append(tmp)
            #第3-3层，找到表2的内容 
            table_dict2 = []
            box_mm_tabel2_tbody_2 = soup_mm_tabel2.find_all("td")
            column_num = len(thead_list2)
            if len(box_mm_tabel2_tbody_2)%column_num == 0:
                tmp = ""
                tmp_list = []
                for i in range(len(box_mm_tabel2_tbody_2)):
                    table_dict2.append(box_mm_tabel2_tbody_2[i].string)
            #保存数据
            Save_data(manufacturer, brand, series, model_id_dict[id], thead_list1, table_dict1, thead_list2, table_dict2, url_maintenance)
            print u"正在保存第%d车系(%d-%d)的第%d个车型(%d-%d):%s-%s-%s" %(num_car_model, num_car_model,num_url_car, num_car_tmp, num_car_tmp, num_car,
                                                                         manufacturer, brand, series)
            num_car_tmp += 1
        #maintenance_dict[id] = [model_id_dict[id], thead_list, table_dict]
        return None
    #return manufacturer,brand,series,maintenance_dict

if __name__ == "__main__":
    url = "http://db.auto.sohu.com/maint_list.shtml"
    #获取每个车型保养配置的地址
    url_car = Getcarurl(url)
    #获取每个车型的具体保养配置
    num_url_car = len(url_car)
    db=ConnectDB()
    db.dbcreate()
    bad_url = []
    for i in range(num_url_car):
        bad_url.append(GetMaintenance(url_car[i],i, num_url_car))
    pd.DataFrame(bad_url).to_csv("bad_url.txt")
    
    