# coding=utf-8
import requests
import json
import pandas as pd
import numpy as np
import time
import sched
from threading import Thread
import rqdatac as rd
from datetime import timedelta
from datetime import datetime

rd.init()


class GuBaUpdate(object):
    rd_stock_info = rd.all_instruments('CS', date='2018-01-01')
    rd_stock_info = rd_stock_info[rd_stock_info['status'] == 'Active']

    def __init__(self, login_type='normal'):
        self.__login_type = login_type
        if self.__login_type == 'normal':
            self.__login_url = 'https://api.ssymmetry.com/api/public/user/login'
        else:
            self.__login_url = 'https://beta.ssymmetry.com/api/public/user/login'
        self.schedule = sched.scheduler(time.time, time.sleep)
        th = Thread(target=self.__reconnect)
        th.start()
        time.sleep(4.0)
        # 关于2018年1月1日活跃的普通股

    def __reconnect(self):
        login_info = requests.put(
            url=self.__login_url,
            data=json.dumps({
                'username': 'wang.tao@ricequant.com',
                'password': 'sS+mmetry20181010'
            })
        ).json()
        self.cookies = '-'.join(['user', login_info['user_id'], login_info['token']])
        print("\n!!!Reconnect API!!! Cookies: {}\n".format(self.cookies))
        self.schedule.enter(3540, 0, self.__reconnect)
        self.schedule.run()

    def hourly_factor_1_hour(self, date_time=None, write_csv=True,
                             path='//home//rice//Zirui_Wei_factor_test//EastMoney_hourly//'):
        """
        获取指定日期指定小时的东方财富股吧小时级别舆情数据构成的pd.df
        每个整点运行一次
        :param date_time: str 形如'2018-11-28 17:00:00'.
        默认是比当前时间滞后两个小时，再向前取整到整点
        :param write_csv: 是否输出csv
        :param path: 以'//'结尾的csv存储路径，默认为plato上的EastMoney_hourly文件夹
        :return: pd.df
        """
        if date_time is None:
            current_time = datetime.now()
            previous_time = current_time - timedelta(hours=2)
            previous_time = previous_time - timedelta(minutes=previous_time.minute,
                                                      seconds=previous_time.second)
            date_time = previous_time.strftime('%Y-%m-%d %H:%M:%S')
        else:
            pass
        data = requests.post(
            url='https://api.ssymmetry.com/api/gub/sentiment/hour',
            data=json.dumps({
                'start': date_time,
                'end': date_time
            }),
            headers={
                'Authorization': self.cookies
            }
        ).json()
        data = self.reformat_json_list(data)
        if write_csv:
            date_time = date_time.replace(':', '-')
            data.to_csv(path + date_time + '.csv')
        else:
            pass
        return data

    @staticmethod
    def reformat_json_list(json_list, data_key='sentiment_index_hourly',
                           matching_key='stock_code'):
        """
        把json返回的list转换成DataFrame
        :param json_list: 需要转换的json list
        :param data_key: 对应于data的key
        :param matching_key: 需要与data展开后的数据对应的key
        :return: pd.df
        """
        temp1 = [d[data_key] for d in json_list]
        temp_data = [t for T in temp1 for t in T]
        temp_matching_keys = [d[matching_key] for d in json_list]
        temp_matching_times = list(map(lambda x: len(x[data_key]), json_list))
        matching = np.repeat(temp_matching_keys, temp_matching_times)
        all_data = pd.DataFrame(temp_data)
        all_data['matching_key'] = matching
        return all_data

    def daily_factor_1_day(self, date=None, write_csv=True,
                           path='F://ricequant_internship//1215'):
        """
        获取指定日期的东方财富股吧日级别舆情数据构成的pd.df
        每天06:00运行一次
        :param date: 形如'2018-11-27 的str
        :param write_csv: 是否输出csv，默认为True
        :param path: 以'//'结尾的csv存储路径，默认为plato上的EastMoney_daily文件夹
        :return: pd.df
        """
        if date is None:
            date = datetime.now().date() - timedelta(days=1)
            date = str(date)
        else:
            pass
        data0 = requests.post(
            url='https://api.ssymmetry.com/api/gub/sentiment/day',
            data=json.dumps({
                'date': date
            }),
            headers={
                'Authorization': self.cookies
            },
        ).json()
        data1 = pd.DataFrame(data0)
        if write_csv:
            date = date.replace(':', '-')
            data1.to_csv(path + date + '.csv', encoding='utf-8_sig')
        else:
            pass
        return data1

