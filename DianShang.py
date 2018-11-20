import json
import requests
import time
import sched
from threading import Thread
import pandas as pd
from datetime import datetime
from dateutil.relativedelta import relativedelta


class DianShang(object):
    def __init__(self):
        self.__login_url = 'https://api.ssymmetry.com/api/public/user/login'
        self.schedule = sched.scheduler(time.time, time.sleep)
        th = Thread(target=self.__reconnect)
        th.start()
        time.sleep(1.5)
        self.dian_shang_info = requests.post(
            url='https://api.ssymmetry.com/api/v1/brands/info',
            headers={
                'Authorization': self.cookies
            }
        ).json()
        self.dian_shang_info = pd.DataFrame(self.dian_shang_info)
        self.dian_shang_info.index = self.dian_shang_info[3]

    def __reconnect(self):
        login_info = requests.put(
            url=self.__login_url,
            data=json.dumps({
                'username': 'wang.tao@ricequant.com',
                'password': 'sS+mmetry20181010'
            })
        ).json()
        self.cookies = '-'.join(['user', login_info['user_id'], login_info['token']])
        print("\n!!!{} Reconnected API!!! Cookies: {}\n".format(self.__class__, self.cookies))
        self.schedule.enter(3540, 0, self.__reconnect)
        self.schedule.run()

    def categorical_factor(self, stock_code, start_date='2016-01-01', end_date='2018-03-31'):
        final_result = []
        temp_bid = str(self.dian_shang_info.ix[stock_code][0])
        cur_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        while str(cur_date) <= end_date:
            new_cur_date = cur_date + relativedelta(days=31)
            result = requests.post(
                url='https://api.ssymmetry.com/api/v3/brand/product/sale',
                data=json.dumps({
                    'start': str(cur_date),
                    'end': max(str(new_cur_date), end_date),
                    'bid': temp_bid
                }),
                headers={
                    'Authorization': self.cookies
                },
            ).json()
            final_result = final_result + result
            cur_date = new_cur_date
        final_result = pd.DataFrame(final_result)
        final_result.columns = ['date', 'brand', 'category', 'sales']
        return final_result
