# 导入函数库
import jqdata
import numpy as np
import pandas as pd
import datetime
import time
#import statsmodels.api as sm
from sklearn import linear_model
from sklearn.preprocessing import Imputer
# 初始化函数，设定基准等等
def initialize(context):
    # 设定沪深300作为基准
    set_benchmark('000300.XSHG')
    # 开启动态复权模式(真实价格)
    set_option('use_real_price', True)
    
    # 过滤掉order系列API产生的比error级别低的log
    # log.set_level('order', 'error')
    
    set_option('use_real_price',True) # 用真实价格交易
    log.set_level('order','error')    # 设置报错等级
    ### 股票相关设定 ###
    # 股票类每笔交易时的手续费是：买入时佣金万分之三，卖出时佣金万分之三加千分之一印花税, 每笔交易佣金最低扣5块钱
    set_order_cost(OrderCost(close_tax=0.001, open_commission=0.0003, close_commission=0.0003, min_commission=5), type='stock')
    set_pas()    #1设置策略参数
    set_variables() #2设置中间变量
    
    ## 运行函数（reference_security为运行时间的参考标的；传入的标的只做种类区分，因此传入'000300.XSHG'或'510300.XSHG'是一样的）
      # 开盘前运行
    run_daily(before_market_open, time='before_open', reference_security='000300.XSHG') 
      # 开盘时运行
    run_daily(market_open, time='open', reference_security='000300.XSHG')
      # 收盘后运行
    run_daily(after_market_close, time='after_close', reference_security='000300.XSHG')

def set_pas():
    g.tc = 7  # 设置调仓天数
    g.num_stocks = 5  # 设置每次调仓选取的股票数量
    # 定义股票池，上证180指数成分股
    g.index='000010.XSHG'
    g.stocks = get_index_stocks(g.index)

#设置中间变量
def set_variables():
    g.t = 0 #记录回测运行的天数
    g.if_trade = False #当天是否交易
    
#设置回测条件
def calAt(stock,date,n):
    #计算股票stock的n日均线因子
    #用于计算当期因子值
    #输入参数：stock：股票代码；date:计算日期；n:计算日期前n天
    price = get_price(stock,end_date=date, frequency='daily', fields='close', skip_paused=True, fq='pre', count=n)
    At = mean(price)
    Atadjust = At/price.tail(1)
    Atadjust = Atadjust.iloc[0,0]
    return Atadjust
#返回值


