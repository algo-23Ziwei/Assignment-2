## 开盘前运行函数     
def before_market_open(context):
    if g.t%g.tc==0:
        #每g.tc天，交易一次行
        g.if_trade=True 
        # 设置手续费与手续费
        # set_slip_fee(context)
    
## 开盘时运行函数
def market_open(context):
    log.info(g.t, g.tc, g.if_trade)
    date = context.current_dt
    if g.if_trade == True:
        # 依本策略的买入信号，得到应该买的股票列表
        MS_should_buy = SortStockList(g.stocks,date).tail(5).index
        log.info(MS_should_buy)
        # 计算现在的总资产，以分配资金，这里是等额权重分配 返回一个数
        MonPerStock=context.portfolio.portfolio_value/g.num_stocks
        # 得到当前持仓中可卖出的股票
        if len(context.portfolio.positions)>0:
            #当持仓不为零时，剔除持仓股票中停牌股即可 返回list
            holding = context.portfolio.positions
        else:
            # 当持仓为0时，可卖出股票为0 返回list
            holding = []
        # 对于不需要持仓的股票，全仓卖出
        for stock in holding:
            if stock not in MS_should_buy:
                order_target_value(stock, 0)
        # 对于需要持仓的股票，按分配到的份额买入
        for stock in MS_should_buy:
            order_target_value(stock, MonPerStock)
    g.if_trade = False
    
## 收盘后运行函数  
def after_market_close(context):
    g.t+=1
    log.info(str('函数运行时间(after_market_close):'+str(context.current_dt.time())))
    #得到当天所有成交记录
    trades = get_trades()
    for _trade in trades.values():
        log.info('成交记录：'+str(_trade))
    log.info('一天结束')
    log.info('##############################################################')

    pass
