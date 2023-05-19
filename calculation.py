#计算训练集
def calATlist(stock,date,n):
    lastDate = date
    #lastDate = datetime.datetime.strptime(date, '%Y-%m-%d')
    #输入时间为date
    delta = datetime.timedelta(days=7)
    lastDate = lastDate - delta
    #往前推一周 计算训练用 AT因子，（因为要用前一周的因子和当周的收益率回归）
    At = []
    for i in range(25):
        temp = calAtevery(stock,lastDate,n)
        At.append(temp.iloc[0,0])
        lastDate = lastDate - delta
    return At
 
def calEstYeild(stock,date):
    k = [3, 5, 10, 20, 30, 60,90,120, 180, 240, 270, 300]
    ATlist=[]
    #计算 前25个单位时间内各长度的均线因子 以及 收益率
    df = pd.DataFrame()
    for item in k:
        df['%s'%item]=calATlist(stock,date,item)
    #将收益率序列添加到最后一列    
        df['rflist']=calRFlist(stock,date)
        
    #计算用于 预测输入的因子值
    st = [1,2,3,4,5,6,7,8,9,10,11,12]
    for i,item in enumerate(k):
        st[i] = calAt(stock,date,item)
        
        #线性回归部分
    
    #imp = Imputer(missing_values='NaN',strategy='mean',axis=0,verbose=0,copy=True)
    #df = imp.fit_transform(df)
    #df = pd.DataFrame(df)
    #df.columns = ['3','5','10','20','30','60','90','120','180','240','270','300','rflist']
    
    #log.info(df)
    
    y = df['rflist']
    x = df[['3','5','10','20','30','60','90','120','180','240','270','300']]
    clf = linear_model.LinearRegression()
    clf.fit(x,y)
    yhat = clf.predict(st)
    #x = sm.add_constant(x)#添加截距项
    #est = sm.OLS(y,x).fit()
    #est.summary() #看统计量结果
    #est.params #查看回归参数
    #预测收益率
    #yhat = est.predict(st)
    return yhat
   
def calRFlist(stock,date):
    #计算收益率序列
    nowDate = date
    #nowDate = datetime.datetime.strptime(date, '%Y-%m-%d')
    delta = datetime.timedelta(days=7)
    rflist = []
    for i in range(25):
        weekprice = get_price(stock,end_date=nowDate,frequency='daily',fields=['close','open'],count=5,skip_paused=True)
        cp = weekprice.iloc[1,-1]
        op = weekprice.iloc[2,1]
        rf = (cp-op)/op
        rflist.append(rf)
        nowDate = nowDate - delta
    return rflist   

def SortStockList(stocks,date):
    df = pd.DataFrame()
    for stock in stocks:
        df['%s'%stock] = calEstYeild(stock,date)
    df = df.T
    stockListSorted = df.sort(columns=0)
    return stockListSorted

def set_slip_fee(context):
    # 将滑点设置为0
    set_slippage(FixedSlippage(0)) 
    # 根据不同的时间段设置手续费
    dt=context.current_dt
    log.info(type(context.current_dt))
    
    if dt>datetime.datetime(2013,1, 1):
        set_commission(PerTrade(buy_cost=0.0003, sell_cost=0.0003, min_cost=5)) 
        
    elif dt>datetime.datetime(2011,1, 1):
        set_commission(PerTrade(buy_cost=0.001, sell_cost=0.002, min_cost=5))
            
    elif dt>datetime.datetime(2009,1, 1):
        set_commission(PerTrade(buy_cost=0.002, sell_cost=0.003, min_cost=5))
                
    else:
        set_commission(PerTrade(buy_cost=0.003, sell_cost=0.004, min_cost=5))    
