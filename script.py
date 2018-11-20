import json
import requests
import pandas as pd
from DianShang import DianShang
#
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
# data0 = requests.post(
#     url='https://api.ssymmetry.com/api/gub/sentiment/day',
#     data=json.dumps({
#         'date': '2018-11-01'
#     }),
#     headers={
#         'Authorization': cookies
#     },
# ).json()
#
# # ==============================================================================
# # 2018-11-07
# stock_info = rd.all_instruments('CS')
# # 电商=========================================================================
# dian_shang_info = requests.post(
#     url='https://api.ssymmetry.com/api/v1/brands/info',
#     headers={
#         'Authorization': guba1.cookies
#     }
# ).json()
#
# dian_shang_info = pd.DataFrame(dian_shang_info)
# dian_shang_info.index = dian_shang_info['3']
#
# hua_di_1 = requests.post(
#     url='https://api.ssymmetry.com/api/v3/brand/product/sale',
#     data=json.dumps({
#         'start': '2018-03-01',
#         'end': '2018-03-31',
#         'bid': str(dian_shang_info.ix['002035'][0])
#     }),
#     headers={
#         'Authorization': guba1.cookies
#     },
# ).json()
#
# hua_di_1 = pd.DataFrame(hua_di_1)

#=======================================
dian_shang_1 = DianShang()
dianshang_data = dian_shang_1.categorical_factor(stock_code='002035', start_date='2016-01-01', end_date='2018-03-31')

import seaborn