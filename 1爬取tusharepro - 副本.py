# -*- coding: utf-8 -*-
import tushare as ts
import pandas as pd
import requests
import sys
import time
import datetime
dateToday = datetime.date.today().strftime('%Y%m%d')
token="c8811a29e9b51d03b2b3f6be3937f331d6187999563900664056c438"
ts.set_token(token)
pro=ts.pro_api()
url = []
df=pd.read_csv("set/codelist_del_st.csv",encoding="unicode_escape")
alist=df.code.tolist()
for i in alist:
    x="%06d" % i
    if x[0]=="6":url.append('%s.SH'%x)
    else:url.append('%s.SZ'%x)
l=len(url)
y=0
while y<l:
    c=url[y]
    df1=pro.daily(ts_code=c,start_date='20170101',end_date=dateToday)
    df1.to_csv("data/%s.csv"%c)
    y=y+1
    time.sleep(1)
    
