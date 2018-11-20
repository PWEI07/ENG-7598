from SnowBall import *
import rqdatac as rd
rd.init()

stocks_info = rd.all_instruments(type='CS', date='20180802')
stocks_id = list(map(lambda x: x[:6], stocks_info['order_book_id']))  # stock codes without suffix
trading_dates = rd.get_trading_dates('2018-01-01', '2018-11-01')


my_snow_ball = SnowBall()
df1 = my_snow_ball.get_interval_raw_factor(trading_dates)
df2 = df1[stocks_id]
# req1 = my_snow_ball.__hourly_factor_1_day('2018-10-01')
#
# my_snow_ball.__reconnect()
#
#
#
#
#
#
#
# req1 = requests.post(
# url = 'https://betaj.ssymmetry.com/api/v4/sentiment/xueqiu/queryByDay',
# data = json.dumps({
# 'date': '2018-10-01',
# 'sort': 1
# }),
# headers = {
# 'Authorization': cookies,
# 'content-type': 'application/json'
# }
# ).json()

