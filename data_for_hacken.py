import requests
import json

login_info = requests.put(
    url='https://api.ssymmetry.com/api/public/user/login',
    data=json.dumps({
        'username': 'wang.tao@ricequant.com',
        'password': 'sS+mmetry20181010'
    })
).json()

cookies = '-'.join(['user', login_info['user_id'], login_info['token']])

e_commerce_info = requests.post(
    url='https://api.ssymmetry.com/api/v1/brands/info',
    headers={
        'Authorization': cookies
    }
).json()

# ao jia hua
for i in e_commerce_info:
    if i[3] == '002614':
        ajh_info = i
# rong tai jian kang
for i in e_commerce_info:
    if i[3] == '603579':
        rtjk_info = i

rtjk_1 = requests.post(
    url='https://api.ssymmetry.com/api/v2/brand/seq/sale',
    data=json.dumps({
        'start': '2018-03-01',
        'end': '2018-03-31',
        'bid': str(rtjk_info[0])
    }),
    headers={
        'Authorization': cookies
    },
).json()

rtjk_2 = requests.post(
    url='https://api.ssymmetry.com/api/v3/brand/seq/sale',
    data=json.dumps({
        'start': '2017-01-01',
        'end': '2018-11-05',
        'bid': str(rtjk_info[0])
    }),
    headers={
        'Authorization': cookies
    },
).json()

# data0 = requests.post(
#     url='https://api.ssymmetry.com/api/gub/sentiment/day',
#     data=json.dumps({
#         'date': '2018-10-01'
#     }),
#     headers={
#         'Authorization': guba1.cookies
#     },
# ).json()

data = requests.post(
            url = 'https://api.ssymmetry.com/api/hour/gub/sentiment',
            data = json.dumps({
            'stock_code': '000622',
            'start': '2018-08-02',
            'end': '2018-08-02',
            'sort': 1
            }),
            headers = {
            'Authorization': cookies
            },
            ).json()