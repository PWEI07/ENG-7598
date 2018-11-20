from GuBa import GuBa
import rqdatac as rd
rd.init()

# test get one day data
guba1 = GuBa()
# s1 = guba1.__hourly_factor_1_day('2018-08-02')

# test get period data
trading_dates = rd.get_trading_dates('2017-10-01', '2018-11-12')
sentiment_factor = guba1.daily_factor(trading_dates)


# select only common stocks
def selected_active_stocks(df, col_name):
    df1 = df[['date', col_name, 'stock_code']].copy()
    df1 = df1.pivot(index='date', columns='stock_code', values=col_name)
    stock_codes = []
    original_stock_codes = []
    rd_stock_info = rd.all_instruments('CS', date='2018-01-01')
    rd_stock_info = rd_stock_info[rd_stock_info['status'] == 'Active']
    rd_stock_codes = list(rd_stock_info['order_book_id'])
    for i in list(df1.columns):
        try:
            if rd.id_convert(i) in rd_stock_codes:
                stock_codes.append(rd.id_convert(i))
                original_stock_codes.append(i)
        except:
            pass
    df1 = df1[original_stock_codes]
    df1.columns = stock_codes
    return df1


sentiments_2 = selected_active_stocks(sentiment_factor, 'sentiment_index')
sentiments_2.to_pickle('F://ricequant_internship//ENG-7598//my_data//sentiments_1112.pkl')

# data0 = guba1.__daily_factor_1_day('2017-10-08')


