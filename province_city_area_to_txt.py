# !py
# -*- encoding: utf-8 -*-
'''
@file      : province_city_area_to_txt.py
@comments  : 
@time      : 2022/01/24
@author    : Jacob Zhou <jacob.zzh@outlook.com>
@ver       : 1.0
'''

import requests
from bs4 import BeautifulSoup
import time
import json

class GetCitysToLocal(object):
    def __init__(self):

        # 设置元数据年份
        self.year = 2021

        # 生成省市区txt文件
        self.getSSQ()

    @staticmethod
    def get_response(url, attr):
        response = requests.get(url)
        response.encoding = response.apparent_encoding  # 编码转换
        response.text[:1000]
        soup = BeautifulSoup(response.text, features="html.parser")
        table = soup.find_all('tbody')[1].tbody.tbody.table
        if attr:
            trs = table.find_all('tr', attrs={'class': attr})
        else:
            trs = table.find_all('tr')
        return trs

    # 创建文件
    # file_path：文件路径
    # msg：即要写入的内容
    @staticmethod
    def create_file(file_path, msg):
        f = open(file_path, "a", encoding='utf-8')
        json.dump(json.dumps(msg, ensure_ascii=False),f, ensure_ascii=False)
        f.close

    def getSSQ(self):
        # 年份
        print('Get data of year - ' + str(self.year))
        base_url = 'http://www.stats.gov.cn/tjsj/tjbz/tjyqhdmhcxhfdm/%s/' % self.year
        trs = self.get_response(base_url, 'provincetr')
        areas = []
        for tr in trs:  # 循环每一行
            # 循环每个省
            i = 0
            for td in tr:
                if td.a is None:
                    continue
                href_url = td.a.get('href')
                province_name = td.a.get_text()
                # province_code = str(href_url.split(".")[0])
                province_url = base_url + href_url

                i +=1

                # 循环每个市
                trs = self.get_response(province_url, None)
                j = 0
                for tr in trs[1:]:
                    city_code = tr.find_all('td')[0].string
                    city_code = city_code[0:3]
                    city_name = tr.find_all('td')[1].string

                    j +=1

                    # 循环每个区县
                    city_url = base_url + tr.find_all('td')[1].a.get('href')
                    trs = self.get_response(city_url, None)
                    for tr in trs[1:]:
                        county_code = tr.find_all('td')[0].string
                        county_code = county_code[0:5]
                        county_name = tr.find_all('td')[1].string

                        county = {}
                        county["province"] = province_name
                        county["city"] = city_name
                        county["value"] = county_name

                        print(province_name + '-' + city_name + '-' + county_name)
                        areas.append(county)
                time.sleep(.5)
            # 等待,防止无响应
        # print(str(areas))

        self.create_file('./area.json',str(areas))

if __name__ == '__main__':
    GetCitysToLocal()
