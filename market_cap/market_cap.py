import requests
from requests import Request, Session
import json
import pandas as pd
import time
from datetime import datetime

with open('market_cap_id.json','r') as r:
    data = json.load(r)
    filter_sym_id = data['filter_sym_id']
    symbols = data['symbols']

symbol_list = [sym.split('binance.')[1].split('_')[0] for sym in symbols]
for i in symbol_list:
    if i not in filter_sym_id.keys():
        print(i)

cap = {}
period = 200 # coinmarket cap拿数据如果period设置太少，会变成1小时周期。其次coinmarket cap的数据会做二次校正
date_update = str(datetime.now()).split(':')[0].replace('-','')+'08'
check_dt = int(datetime(datetime.now().year,datetime.now().month,datetime.now().day,8).timestamp()) # 这里如果机子是utc时间，要把8改成0
symbol_list = [sym.split('binance.')[1].split('_')[0] for sym in symbols]
base_url = 'https://api.coingecko.com/api/v3/coins/'

for sym in symbol_list:

    print(filter_sym_id[sym][0])   # 这里正常第一个是对的
    url = base_url + filter_sym_id[sym][0]+"/market_chart?vs_currency=usd&days="+str(period)
    print(url)
    session = Session()
    session.headers.update()
    market_cap_response = session.get(url)
    print(market_cap_response)
    cap_data = json.loads(market_cap_response.text)

    df =  pd.DataFrame(cap_data['market_caps'])

    df[0] = (df[0]//86400*86400/1000).astype(int)

    cap[sym] = df.set_index(0)
    time.sleep(4)# 防止被ban

cap_d = pd.DataFrame()
name_list = []
for i in cap.keys():
    name_list.append(i)
    cap_d = pd.concat([cap_d,cap[i]],axis=1)
    cap_d.columns = name_list


cap_d.rename(columns={'shib':'1000shib'},inplace=True)
list_c = []
for c in cap_d.columns:
    list_c.append('binance.'+c+'_usdt_swap')
cap_d.columns = list_c
cap_d.to_hdf('market_cap.h5',key = 'mc')




