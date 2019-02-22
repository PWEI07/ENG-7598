# 可以自己import我们平台支持的第三方python模块，比如pandas、numpy等。
import pandas as pd
# 在这个方法中编写任何的初始化逻辑。context对象将会在你的算法策略的任何方法之间做传递。


def init(context):
    # context内引入全局变量s
    context.period = 10 # 换仓期
    context.counter = 0 # 用于计数
    # 初始化时订阅合约行情。订阅之后的合约行情会在handle_bar中进行更新。
    logger.info("RunInfo: {}".format(context.run_info))
    # 读入情绪指数数据
    context.sentiment_index = pd.read_pickle('F://ricequant_internship//1211//sentiment_index_1211.pkl')
    # context.current_pool = pd.Series(data = 0.0, index=context.sentiment_index.columns)
    context.fired = False


# before_trading此函数会在每天策略交易开始前被调用，当天只会被调用一次
def before_trading(context):
    print('Run before_trading: ', context.now, '\n')
    if context.counter % context.period == 0 and not context.fired:
        context.adjust = True  # flag 是否需要调仓

        recent_sentiment = context.sentiment_index.loc[str(context.now.date()), :]  # 获取各股票当前最新sentiment_index
        new_pool = recent_sentiment >= recent_sentiment.quantile(0.0)
        new_pool = new_pool.apply(lambda x: 1.0 if x else 0)
        new_pool /= sum(new_pool)  # 本期目标持仓

        current_pool = pd.Series(data=0.0, index=context.sentiment_index.columns)
        for i in context.portfolio.positions.keys():
            current_pool[i] = context.portfolio.positions[i].value_percent

        context.order_percent = new_pool - current_pool  # 本期目标持仓减去当前持仓得到本期需要买或者卖的比例
        context.order_percent = context.order_percent[context.order_percent != 0]
        context.order_percent.sort_values(ascending=True, inplace=True)
    else:
        context.adjust = False


# 你选择的期货数据更新将会触发此段逻辑，例如日线或分钟线更新
def handle_bar(context, bar_dict):
    # if not context.adjust and not context.fired:
    #     # 如果不是换仓期，则直接跳过
    #     return
    if context.adjust and not context.fired:
        print('Adjust: ', context.now, '\n')
        # logger.info(context.order_percent)
        # logger.info(type(context.order_percent))
        for i in context.order_percent.index:
            # logger.info(i)
            # logger.info(context.order_percent[i])
            order_percent(i, context.order_percent[i])
        context.fired = True
        context.adjust = False
    # logger.info("\nbar_dict[context.s]: {}\n".format(bar_dict[context.s]))
    # temp_order = order_target_percent(context.s, 0.2, style=LimitOrder(bar_dict[context.s].open * 1.002))
    # temp_order = sell_open(context.s, 1)
    # logger.info("\ntemp_order: {}\n".format(temp_order))
    # temp_order = order_shares('000001.XSHE', 100, style=MarketOrder())
    # logger.info("\ntemp_order: {}\n".format(temp_order))
    # context.fired1 = True
    #
    #     # TODO: 开始编写你的算法吧！
    # if context.count > 4 and not context.fired2:
    #     logger.info("\nbar_dict[context.s]: {}\n".format(bar_dict[context.s]))
    #     temp_order = buy_close(context.s, 1)
    #     # temp_order = order_shares(context.s, -100, style=MarketOrder())
    #     logger.info("\ntemp_order: {}\n".format(temp_order))
    #     context.fired2 = True
# after_trading函数会在每天交易结束后被调用，当天只会被调用一次
def after_trading(context):
    print('Run after_trading: ', context.now, '\n')
    context.counter += 1

