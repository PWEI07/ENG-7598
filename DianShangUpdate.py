import json
import requests
import pandas as pd
from datetime import datetime
from datetime import timedelta
from dateutil.relativedelta import relativedelta


class DianShangUpdate(object):

    def __connect(self):
        login_info = requests.put(
            url=self.__login_url,
            data=json.dumps({
                'username': 'wang.tao@ricequant.com',
                'password': 'sS+mmetry20181010'
            })
        ).json()
        self.cookies = '-'.join(['user', login_info['user_id'], login_info['token']])
        self.__connect_time = datetime.now()
        print('DianShang cookies: ', self.cookies)

    def __check_connect(self):
        if (datetime.now() - self.__connect_time).seconds > 3300:
            self.__connect()

    def __init__(self):
        self.__login_url = 'https://api.ssymmetry.com/api/public/user/login'
        self.__connect()

        self.dian_shang_info = requests.post(
            url='https://api.ssymmetry.com/api/v1/brands/info',
            headers={
                'Authorization': self.cookies
            }
        ).json()

        self.dian_shang_info = pd.DataFrame(self.dian_shang_info)
        self.dian_shang_info.index = self.dian_shang_info[3]
        self.all_bids = list(self.dian_shang_info[0])

    def __short_periodic_sales(self, start_date='2018-12-10', end_date='2018-12-15'):

        self.__check_connect()
        data0 = list(map(lambda x: requests.post(
            url='https://api.ssymmetry.com/api/v2/brand/seq/sale',
            data=json.dumps({
                'start': start_date,
                'end': end_date,
                'bid': x
            }),
            headers={
                'Authorization': self.cookies
            },
        ).json(), self.all_bids))
        return data0

    def periodic_sales(self, start_date='2016-01-01', end_date='2018-12-15'):
        """
        给定起始日期和终止日期，先将日期划分，取得所有电商时间段内销售额，最后拼接为pd.df
        :param start_date: 起始时间，形如'2016-01-01'
        :param end_date: 截止时间，形如'2018-03-31'
        :return: pd.df
        """
        cur_date = datetime.strptime(start_date, '%Y-%m-%d').date()
        start_dates = []
        end_dates = []
        while str(cur_date) <= end_date:
            start_dates.append(str(cur_date))
            end_dates.append(min(end_date, str(cur_date + relativedelta(days=30))))
            cur_date += relativedelta(days=31)
        final_result = list(map(lambda x, y: self.__short_periodic_sales(x, y), start_dates, end_dates))
        final_result = [t_small for T in final_result for t in T for t_small in t]
        final_result = pd.DataFrame(final_result)
        final_result.columns = ['date', 'brand', 'sales', 'Tmall']
        return final_result

    def update_periodic_sales(self, date=None, write_csv=True, path='/mnt//ftp//online_retailer//periodic_sales//'):
        """
        return online retailer sales in a specific date
        :param date: default two days earlier from now
        :param write_csv: whether to output a csv
        :return: pd.df
        """
        if date is None:
            date = datetime.now().date() - timedelta(days=2)
            date = str(date)
        else:
            pass

        final_result = self.__short_periodic_sales(date, date)
        final_result = [t for T in final_result for t in T]
        final_result = pd.DataFrame(final_result)
        final_result.columns = ['date', 'brand', 'sales', 'Tmall']
        if write_csv:
            final_result.to_csv(path + date + '.csv', encoding='utf-8_sig')
        return final_result

dianshang_update1 = DianShangUpdate()
test_data = dianshang_update1.update_periodic_sales(date='2018-12-22', path='F://ricequant_internship//SP-151//online_retailer//periodic_sales//')