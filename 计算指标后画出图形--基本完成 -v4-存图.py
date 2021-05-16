
import tushare as ts
from datetime import datetime
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import mpl_finance as mpf
import seaborn as sns
import talib as tl

code=input("请输入代码（sh,sz）：")
df = pd.read_csv("D://7star//kdata//%s.csv"%code)
df['date']=df['trade_date']
df['date']=pd.to_datetime(df['date'], format='%Y%m%d')
df = df.sort_values('date')
df = df.set_index('date')#将“date”设置为index
# 导入数据 - 注意：这里请填写数据文件在您电脑中的路径
stock_data = df

# ========== 计算移动平均线
# 分别计算5日、20日、60日的移动平均线
ma_list = [5, 10, 30]
# 计算指数平滑移动平均线EMA
for ma in ma_list:
    stock_data['EMA_' + str(ma)] = pd.DataFrame.ewm(stock_data['close'], span=ma)




# ========== 将算好的数据输出到csv文件 - 注意：这里请填写输出文件在您电脑中的路径
stock_datas=stock_data
for ma in ma_list:
    stock_datas['MA_' + str(ma)] = np.round(pd.Series.rolling(stock_datas['close'], window=ma).mean(), 1)
 
low_list = stock_datas['low'].rolling(34, min_periods=9).min()
low_list.fillna(value=stock_datas['low'].expanding().min(), inplace=True)
high_list = stock_datas['high'].rolling(34, min_periods=9).max()
high_list.fillna(value=stock_datas['high'].expanding().max(), inplace=True)
rsv = (stock_datas['close'] - low_list) / (high_list - low_list) * 100
 
stock_datas['K'] = pd.Series.ewm(rsv, com=2).mean()
stock_datas['D'] = pd.Series.ewm(stock_datas['K'], com=2).mean()
stock_datas['J'] = 3 * stock_datas['K'] - 2 * stock_datas['D']
stock_datas['Z'] =pd.Series.ewm(stock_datas['J'], com=2.5).mean()

low_list1 = stock_datas['low'].rolling(55, min_periods=9).min()
low_list1.fillna(value=stock_datas['low'].expanding().min(), inplace=True)
high_list1 = stock_datas['high'].rolling(55, min_periods=9).max()
high_list1.fillna(value=stock_datas['high'].expanding().max(), inplace=True)
stock_datas['S']= (high_list1-stock_datas['close'])/((high_list1 - low_list1))*100

low_list2 = stock_datas['low'].rolling(9, min_periods=9).min()
low_list2.fillna(value=stock_datas['low'].expanding().min(), inplace=True)
high_list2 = stock_datas['high'].rolling(9, min_periods=9).max()
high_list2.fillna(value=stock_datas['high'].expanding().max(), inplace=True)
rsv1 = (stock_datas['close'] - low_list2) / (high_list2 - low_list2) * 50
 
stock_datas['K1'] = pd.Series.ewm(rsv1, com=2).mean()
stock_datas['D1'] = pd.Series.ewm(stock_datas['K1'], com=2).mean()
stock_datas['J1'] = 3 * stock_datas['K1'] - 2 * stock_datas['D1']
#stock_datas['M'] =(stock_datas['J1']>3)&
stock_datas['J2']=stock_datas['J1'].shift(1)
stock_datas['M'] =(stock_datas['J1']>3)&(stock_datas['J2']<=3)

#顶底指标计算：数值上穿关注0.5，底部0.2，清仓卖出3.5，阶段卖出3.2
"""
VAR2=LLV(LOW,10)
VAR3=HHV(HIGH,25)
DDZ
DD= EMA((CLOSE-VAR2)/(VAR3-VAR2)*4,4)
"""
low_list3 = stock_datas['low'].rolling(10, min_periods=9).min()
low_list3.fillna(value=stock_datas['low'].expanding().min(), inplace=True)
high_list3 = stock_datas['high'].rolling(25, min_periods=9).max()
high_list3.fillna(value=stock_datas['high'].expanding().max(), inplace=True)
rsv2 = (stock_datas['close'] - low_list3) / (high_list3 - low_list3) * 4

 
stock_datas['DD'] = pd.Series.ewm(rsv2, com=1.5).mean()#n=4，@=2/n+1,@=

#stock_datas.to_csv("D:\\3shipan\\tdxdata\\603008.csv")
datas=stock_datas.sort_values(by = 'date')


#开始画图
df8 = datas.sort_values('date')
#df8 = datas.set_index('date')#将“date”设置为index
df_last=df8['2020-12-23':]#df_last=df['2020-04-02':'2020-06-29']
df_last.replace(to_replace=True, value=50, inplace=True)#将顶底指标中的判断值true换成50
df_300427=df_last.reset_index()




"""隐藏画K线
fig = plt.figure(figsize=(10, 5))
ax = fig.add_subplot(1, 1, 1)
ax.set_xticks(range(0, len(df_300427['date']), 10))
ax.set_xticklabels(df_300427['date'][::10])
mpf.candlestick2_ochl(ax, df_300427['open'], df_300427['close'], df_300427['high'],
                     df_300427['low'], width=0.6, colorup='r', colordown='g', alpha=0.75);
"""


#加上kd值

sma_5 = df_300427["MA_5"]
sma_10 = df_300427["MA_10"]
sma_30 = df_300427["MA_30"]
df_300427['Z'].fillna(value=0, inplace=True)
df_300427['S'].fillna(value=0, inplace=True)
fig = plt.figure(figsize=(10, 8))
ax = fig.add_axes([0,0.45,1,0.5])
ax2 = fig.add_axes([0,0.2,1,0.2])
ax3 = fig.add_axes([0,0,1,0.2])

ax.set_xticks(range(0, len(df_300427['date']), 10))
ax.set_xticklabels(df_300427['date'][::10])
mpf.candlestick2_ochl(ax, df_300427['open'], df_300427['close'], df_300427['high'],
                      df_300427['low'], width=0.6, colorup='r', colordown='g', alpha=0.75)
plt.rcParams['font.sans-serif']=['Microsoft JhengHei']
Z=round(datas['Z'][-1],2)
S=round(datas['S'][-1],2)
DD=round(datas['DD'][-1],2)
ax.plot(sma_5, label='5日均线')
ax.plot(sma_10, label='10日均线')
ax.plot(sma_30, label='30日均线')
ax2.plot(df_300427['Z'],'r' ,label='Z值:%s'%Z)
ax2.plot(df_300427['S'], 'b',label='S值:%s'%S)
ax2.plot(df_300427['M'],'y')
ax2.set_xticks(range(0, len(df_300427.index), 10))
ax2.set_xticklabels(df_300427.index[::10])

#mpf.volume_overlay(ax3, df_300427['open'], df_300427['close'], df_300427['volume'], colorup='r', colordown='g', width=0.5, alpha=0.8)

ax3.plot(df_300427['DD'], label='顶底:%s'%DD)
ax3.set_xticks(range(0, len(df_300427.index), 10))
ax3.set_xticklabels(df_300427.index[::10])


ax.set_title('%s'%code,fontsize=12,color='r')
ax.legend(loc='upper center', fontsize=12);
ax2.legend(loc='upper center', fontsize=10);
ax3.legend(loc='upper center', fontsize=10);
plt.savefig("C://Users//Administrator//Desktop//大数据研究//pic//%s.png"%code)
plt.show()
