from GuBa import GuBa
import rqdatac as rd
rd.init()

# # test get one day data
# guba1 = GuBa()
#
# sentiment_data = guba1.daily_factor('2017-10-01', '2018-04-01')  # 这一步需要较长时间运行，我已经提前运行了一遍，只要按照下一步所示加载数据就行了
# sentiment_data = guba1.update_daily_factor(sentiment_data)
# sentiment_data.to_pickle('.//sentiment_data.pkl')
# # sentiment_data = pd.read_pickle('.//sentiment_data.pkl')
#
# sentiment_index_factor = GuBa.factor_format(sentiment_data, 'sentiment_index')  # 东方财富情绪指数因子
# post_number_factor = GuBa.factor_format(sentiment_data, 'post_number')  # 东方财富发帖数因子
# read_number_factor = GuBa.factor_format(sentiment_data, 'read_number')  # 东方财富阅读量因子


def test_guba_hourly_data():
    guba1 = GuBa()
    return guba1.hourly_factor('2018-08-03', '2018-08-04')

test_result = test_guba_hourly_data()


guba1 = GuBa()
daily_1128 = guba1.daily_factor('2018-11-28', '2018-11-28')

test_hour = requests.post(
            url='https://api.ssymmetry.com/api/gub/sentiment/hour',
            data=json.dumps({
                'start': '2018-11-28 01:00:00',
                'end': '2018-11-28 12:00:00'
            }),
            headers={
                'Authorization': guba1.cookies
            }
        ).json()

date_time = None
date_time is None
current_time = datetime.now()
previous_time = current_time - timedelta(hours=2)
previous_time = previous_time - timedelta(minutes=previous_time.minute,
                                          seconds=previous_time.second)
previous_time.strftime('%Y-%m-%d %H:%M:%S')