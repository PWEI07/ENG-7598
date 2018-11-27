import requests
import json
import pandas as pd
import numpy as np
import time
import sched
from threading import Thread
import rqdatac as rd
# import rqfactor
# from rqfactor import Factor
from datetime import timedelta
from datetime import datetime
# from bokeh.io import output_notebook
rd.init()


class GuBa(object):
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
        time.sleep(1.0)
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

    def __hourly_factor_1_day(self, date):
        """
        :param date: str %Y-%m-%d
        :return: pd.Series
        """
        result = requests.post(
            url='https://api.ssymmetry.com/api/hour/gub/sentiment/day',
            data=json.dumps({
                'date': date,
                'sort': 1
            }),
            headers={
                'Authorization': self.cookies
            }
        ).json()
        return result

    def hourly_factor(self, dates):
        all_data = []
        for date in dates:
            all_data = all_data + self.__hourly_factor_1_day(str(date))

        all_hourly_data = []
        all_stock_code = []

        for data in all_data:
            all_hourly_data = all_hourly_data + data['sentiment_index_hourly']
            all_stock_code = all_stock_code + [data['stock_code']] * len(data['sentiment_index_hourly'])
        all_data = pd.DataFrame(all_hourly_data)
        all_data['stock_code'] = all_stock_code
        return all_data

    def __daily_factor_1_day(self, date):
        data0 = requests.post(
            url='https://api.ssymmetry.com/api/gub/sentiment/day',
            data=json.dumps({
                'date': date
            }),
            headers={
                'Authorization': self.cookies
            },
        ).json()
        return data0

    def daily_factor(self, start, end):
        temp_start = datetime.strptime(start, '%Y-%m-%d').date()
        temp_end = datetime.strptime(end, '%Y-%m-%d').date()
        temp_delta = temp_end - temp_start
        #         dates = rd.get_trading_dates(start, end)
        all_data = []
        for i in range(temp_delta.days + 1):
            date = temp_start + timedelta(i)
            all_data = all_data + self.__daily_factor_1_day(str(date))
        all_data = pd.DataFrame(all_data)
        all_data.drop(['stock_name'], axis='columns', inplace=True)
        return all_data

    @staticmethod
    def factor_format(df, col_name):
        df1 = df[['date', col_name, 'stock_code']].copy()

        # 将所有舆情数据对应到下一个交易日（节假日期间的舆情数据被除以天数以取到平均值）
        df1['date'] = list(map(lambda x: str(rd.get_next_trading_date(x)), df1['date']))
        df1 = df1.groupby(['date', 'stock_code'])[col_name].apply(
            np.mean).reset_index()

        df1 = df1.pivot(index='date', columns='stock_code', values=col_name)
        stock_codes = []
        original_stock_codes = []
        rd_stock_codes = list(GuBa.rd_stock_info['order_book_id'])
        for i in list(df1.columns):
            try:
                if rd.id_convert(i) in rd_stock_codes:
                    stock_codes.append(rd.id_convert(i))
                    original_stock_codes.append(i)
            except:
                pass
        df1 = df1[original_stock_codes]
        df1.columns = stock_codes
        df1.index = map(lambda x: datetime.strptime(x, '%Y-%m-%d'), df1.index)
        return df1

    # @staticmethod
    # def show_analysis(analysis):
    #     # 对于以下3个index要进行转换，否则会报错
    #     analysis.factor_market_value_distribution.index = list(analysis.factor_market_value_distribution.index)
    #     analysis.ic_market_value_distribution.index = list(analysis.ic_market_value_distribution.index)
    #     analysis.quantile_factor_returns.index = list(analysis.quantile_factor_returns.index)
    #     output_notebook()
    #     analysis.show()
    #
    # @staticmethod
    # def adjustment_period_tunning(df, test_ratio=0.4):
    #     """
    #     对调仓期这一参数进行调参
    #
    #     Args:
    #         df: 以日期为index，以股票代码为column的pandas数据框
    #         test_ratio:测试集所占比例，默认为0.4
    #
    #     Yield:输出最佳的换仓期；显示最佳换仓期在验证集和测试集中的analysis
    #
    #     Return:返回最优换仓周期；验证集因子测试结果；测试集因子测试结果
    #     """
    #
    #     num_validation_rows = np.floor(df.shape[0] * (1 - test_ratio))  # 验证集的行数
    #     q4_accumulate_return = []
    #
    #     for i in np.arange(2, 11):
    #         temp_analysis = factor_analysis(df.iloc[np.arange(num_validation_rows)], period=i, shift_days=0,
    #                                         rank_ic=True, quantile=5, ascending=True, winzorization='percentile',
    #                                         normalization=True, neutralization='industry', include_st=False,
    #                                         include_new=False)
    #         q4_accumulate_return.append(np.product(1 + temp_analysis.quantile_factor_returns.loc['q4']))
    #
    #     optimal_period = np.arange(2, 11)[np.argmax(q4_accumulate_return)]
    #     print("The optimal adjustment period is {}\n".format(optimal_period))
    #     optimal_validation_analysis = factor_analysis(df.iloc[np.arange(num_validation_rows)], period=optimal_period,
    #                                                   shift_days=0, rank_ic=True, quantile=5, ascending=True,
    #                                                   winzorization='percentile', normalization=True,
    #                                                   neutralization='industry', include_st=False, include_new=False)
    #     GuBa.show_analysis(optimal_validation_analysis)
    #     optimal_test_analysis = factor_analysis(df.iloc[np.arange(num_validation_rows, df.shape[0])],
    #                                             period=optimal_period, shift_days=0, rank_ic=True, quantile=5,
    #                                             ascending=True, winzorization='percentile', normalization=True,
    #                                             neutralization='industry', include_st=False, include_new=False)
    #     GuBa.show_analysis(optimal_test_analysis)
    #     return optimal_period, optimal_validation_analysis, optimal_test_analysis

    def update_daily_factor(self, data):
        data_last_date = list(data['date'])[-1]
        data_last_date = datetime.strptime(data_last_date, '%Y-%m-%d')
        data_last_date += timedelta(days=1)
        data_last_date = str(data_last_date.date())
        today = str(datetime.now().date())
        added_data = self.daily_factor(data_last_date, today)
        result = data.append(added_data)
        return result

