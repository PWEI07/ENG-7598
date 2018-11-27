from GuBa import GuBa
import rqdatac as rd
rd.init()

# test get one day data
guba1 = GuBa()

sentiment_data = guba1.daily_factor('2017-10-01', '2018-04-01')  # 这一步需要较长时间运行，我已经提前运行了一遍，只要按照下一步所示加载数据就行了
sentiment_data = guba1.update_daily_factor(sentiment_data)
sentiment_data.to_pickle('.//sentiment_data.pkl')
# sentiment_data = pd.read_pickle('.//sentiment_data.pkl')

sentiment_index_factor = GuBa.factor_format(sentiment_data, 'sentiment_index')  # 东方财富情绪指数因子
post_number_factor = GuBa.factor_format(sentiment_data, 'post_number')  # 东方财富发帖数因子
read_number_factor = GuBa.factor_format(sentiment_data, 'read_number')  # 东方财富阅读量因子







