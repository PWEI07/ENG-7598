# coding=utf-8

import DianShang

dianshang1 = DianShang.DianShang()

data1 = dianshang1.periodic_sales('2016-01-01', '2016-06-30')
data2 = dianshang1.periodic_sales('2016-07-01', '2016-12-31')
data3 = dianshang1.periodic_sales('2017-01-01', '2017-06-30')
data4 = dianshang1.periodic_sales('2017-07-01', '2017-12-31')
data5 = dianshang1.periodic_sales('2018-01-01', '2018-06-30')
data6 = dianshang1.periodic_sales('2018-07-01', '2018-12-17')

data1.to_csv('F://ricequant_internship//SP-151//online_retailer//periodic_sales//20160101_20160630.csv', index=False,
             encoding='utf_8_sig')
data3.to_csv('F://ricequant_internship//SP-151//online_retailer//periodic_sales//20170101_20170630.csv', index=False,
             encoding='utf_8_sig')
data6.to_csv('F://ricequant_internship//SP-151//online_retailer//periodic_sales//20180701_20181215.csv', index=False,
             encoding='utf_8_sig')


data2.to_csv('F://ricequant_internship//SP-151//online_retailer//periodic_sales//20160701_20161231.csv', index=False,
             encoding='utf_8_sig')
data4.to_csv('F://ricequant_internship//SP-151//online_retailer//periodic_sales//20170701_20171231.csv', index=False,
             encoding='utf_8_sig')
data5.to_csv('F://ricequant_internship//SP-151//online_retailer//periodic_sales//20180101_20180630.csv', index=False,
             encoding='utf_8_sig')
# dianshang1_info = dianshang1.dian_shang_info
#
# dianshang_cat1 = dianshang1.categorical_factor('2016-01-01', '2016-06-30')
# dianshang_cat2 = dianshang1.categorical_factor('2016-07-01', '2016-12-31')
# dianshang_cat3 = dianshang1.categorical_factor('2017-01-01', '2017-06-30')
# dianshang_cat4 = dianshang1.categorical_factor('2017-07-01', '2017-12-31')
# dianshang_cat5 = dianshang1.categorical_factor('2018-01-01', '2018-03-31')

# dianshang_cat6 = dianshang1.categorical_factor('2018-12-13', '2018-12-14')

# dianshang_cat1.to_csv('F://ricequant_internship//SP-151//online_retailer//dianshang_cat1.csv')
# dianshang_cat2.to_csv('F://ricequant_internship//SP-151//online_retailer//dianshang_cat2.csv')
# dianshang_cat3.to_csv('F://ricequant_internship//SP-151//online_retailer//dianshang_cat3.csv')
# dianshang_cat4.to_csv('F://ricequant_internship//SP-151//online_retailer//dianshang_cat4.csv')
# dianshang_cat5.to_csv('F://ricequant_internship//SP-151//online_retailer//dianshang_cat5.csv')















# import requests
# import json


# login_info = requests.put(
#     url='https://api.ssymmetry.com/api/public/user/login',
#     data=json.dumps({
#         'username': 'wang.tao@ricequant.com',
#         'password': 'sS+mmetry20181010'
#     })
# ).json()
#
# cookies = '-'.join(['user', login_info['user_id'], login_info['token']])
#
# e_commerce_info = requests.post(
#     url='https://api.ssymmetry.com/api/v1/brands/info',
#     headers={
#         'Authorization': cookies
#     }
# ).json()
#
# # ao jia hua
# for i in e_commerce_info:
#     if i[3] == '002614':
#         ajh_info = i
# # rong tai jian kang
# for i in e_commerce_info:
#     if i[3] == '603579':
#         rtjk_info = i
#
# rtjk_1 = requests.post(
#     url='https://api.ssymmetry.com/api/v2/brand/seq/sale',
#     data=json.dumps({
#         'start': '2018-03-01',
#         'end': '2018-03-31',
#         'bid': str(rtjk_info[0])
#     }),
#     headers={
#         'Authorization': cookies
#     },
# ).json()
#
# rtjk_2 = requests.post(
#     url='https://api.ssymmetry.com/api/v3/brand/seq/sale',
#     data=json.dumps({
#         'start': '2017-01-01',
#         'end': '2018-11-05',
#         'bid': str(rtjk_info[0])
#     }),
#     headers={
#         'Authorization': cookies
#     },
# ).json()
#
# # data0 = requests.post(
# #     url='https://api.ssymmetry.com/api/gub/sentiment/day',
# #     data=json.dumps({
# #         'date': '2018-10-01'
# #     }),
# #     headers={
# #         'Authorization': guba1.cookies
# #     },
# # ).json()
#
# data = requests.post(
#             url = 'https://api.ssymmetry.com/api/hour/gub/sentiment',
#             data = json.dumps({
#             'stock_code': '000622',
#             'start': '2018-08-02',
#             'end': '2018-08-02',
#             'sort': 1
#             }),
#             headers = {
#             'Authorization': cookies
#             },
#             ).json()