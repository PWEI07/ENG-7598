import requests
import json
import pandas as pd
import rqdatac as rd
rd.init()


class SnowBall(object):

    def __init__(self):
        self.login_info = requests.put(
            url='https://beta.ssymmetry.com/api/public/user/login',
            data=json.dumps({
                'username': 'wang.tao@ricequant.com',
                'password': 'sS+mmetry20181010'
            })
        ).json()
        self.cookies = '-'.join(['user', self.login_info['user_id'], self.login_info['token']])

    def reconnect(self):
        self.__init__()

    def get_daily_raw_factor(self, date):
        """
        :param date: str %Y-%m-%d
        :return: dict
        """
        result = requests.post(
            url='https://betaj.ssymmetry.com/api/v4/sentiment/xueqiu/queryByDay',
            data=json.dumps({
                'date': date,
                'sort': 1
            }),
            headers={
                'Authorization': self.cookies,
                'content-type': 'application/json'
            }
        ).json()
        result1 = pd.Series()
        result1.name = date
        for i in result:
            result1[i['stock_code']] = i['sentiment_index']
        return result1

    def get_interval_raw_factor(self, dates):
        # initialize a list
        all_data = []
        # previous_dates: get the nearest recent previous trading dates for all the dates,
        # so as to avoid using future data in factor examination
        previous_dates = list(map(lambda x: rd.get_previous_trading_date(x), dates))
        for date in previous_dates:
            all_data.append(self.get_daily_raw_factor(str(date)))
        result = pd.DataFrame(all_data)
        result.index = dates
        return result