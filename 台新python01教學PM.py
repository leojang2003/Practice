# 台新python01教學PM.py: Python Practices - 01PM (D-G) for 台新銀行
# Jia-Sheng Heh, 07/20/2023, revised from 台新python01A_環境與numpy.py

import os   
wkDir = "c:/Users/Admin/Desktop/台新python/";   os.chdir(wkDir)
print(os.getcwd())

#%%####### (D) Python的數據結構: dict與pd (1.5hr) ##########

#%%##===== (D1).字典(dictionary) =====#####
##== (1).鍵(keys)與值(values)

Xd = dict(customer=["c1","c2"], channel="s1", product=["p1","p2","p3"]);    print("Xd = ",Xd)
     #-- Xd = {'customer': ['c1','c2'], 'channel': 's1', 'product': ['p1','p2','p3'] }
##== (2).鍵(keys)與值(values)
cc = Xd["customer"];   print(cc)   #-- ['c1', 'c2']
pp = Xd["product"];    print(pp)   #-- ['p1', 'p2', 'p3']
print(Xd.keys())     #-- dict_keys(['customer', 'channel', 'product'])
print(Xd.values())   #-- dict_values([['c1', 'c2'], 's1', ['p1', 'p2', 'p3']])
#%%== (3).另一種字典表示法
Xe = {"customer": "c3", "channel": "s2"};     print(Xe)     #-- {'customer': 'c3', 'channel': 's2'}
#%%== (4).修改 (另外還有新增與刪除)
Xd2 = Xd;    Xd3 = Xd.copy();   print("Xd = ",Xd);     print("Xd2 = ",Xd2);     print("Xd3 = ",Xd3)
# Xd =  {'customer': ['c1', 'c2'], 'channel': 's1', 'product': ['p1', 'p2', 'p3']}
# Xd2 =  {'customer': ['c1', 'c2'], 'channel': 's1', 'product': ['p1', 'p2', 'p3']}
# Xd3 =  {'customer': ['c1', 'c2'], 'channel': 's1', 'product': ['p1', 'p2', 'p3']} --> Xd2 和 Xd 其實相同, Xd2改, Xd 也會跟著改
Xd2.update(Xe);       print("Xd = ",Xd);     print("Xd2 = ",Xd2);     print("Xd3 = ",Xd3)
# Xd =  {'customer': 'c3', 'channel': 's2', 'product': ['p1', 'p2', 'p3']}
# Xd2 =  {'customer': 'c3', 'channel': 's2', 'product': ['p1', 'p2', 'p3']}
# Xd3 =  {'customer': ['c1', 'c2'], 'channel': 's1', 'product': ['p1', 'p2', 'p3']}
del Xe["channel"];   print(Xe)   #-- {'customer': 'c3'}

#%%##===== (D2).數據框(dataframe)的創建(create) =====#####
import pandas as pd
##== (1).創建數據框
df1 = pd.DataFrame([[1,2,3],[4,5,6]]);   print("df1=",df1)
# df1=    0  1  2
#      0  1  2  3
#      1  4  5  6
df2 = pd.DataFrame([[1,2,3],[4,5,6]],index=['row1','row2'],columns=['col1','col2','col3']);  print("df2=",df2)
# df2=       col1  col2  col3
#      row1     1     2     3
#      row2     4     5     6
##== (2).由dict創建數據框
Xdf2 = pd.DataFrame(Xd2);   print("Xdf2=",Xdf2)
# Xdf=   customer channel product
#    0       c3      s2      p1
#    1       c3      s2      p2
#    2       c3      s2      p3
## Xdf3 = pd.DataFrame(Xd3);   print("Xdf3=",Xdf3)   #---> error
#%%== (3).最常見的DF創建法
Xdf = pd.DataFrame({"customer": ["c1","c2","c3"], "channel": ["s1","s2","s3"], 
                    "product":["p1","p2","p3"], "quantity": [1,1,2], "amount": [1200,800,3200]});   
print("Xdf = ",Xdf)
# Xdf =    customer channel product  quantity  amount
#        0       c1      s1      p1         1    1200
#        1       c2      s2      p2         1     800
#        2       c3      s3      p3         2    3200

#%%##===== (D3) 數據框架構 =====#####

##== (1).數據框樣貌(shape,head)
print("Xdf.shape =",Xdf.shape)             #-- Xdf.shape = (3, 5) -- (row列數,column行數)
print("Xdf.head(2) =",Xdf.head(2))         #-- 前數行(head)與後數行(tail)
# Xdf.head(2) =   customer channel product  quantity  amount
#               0       c1      s1      p1         1    1200
#               1       c2      s2      p2         1     800
#%%== (2).列索引(index) 與 行/欄位名稱(columns), 及設定/重設索引
Xdf1 = Xdf.copy();            
Xdf1.set_index("customer" , inplace=True);   print(Xdf1)
#          channel product  quantity  amount
# customer                                  
# c1            s1      p1         1    1200
# c2            s2      p2         1     800
# c3            s3      p3         2    3200
print("Xdf1.shape =",Xdf1.shape)             #-- Xdf1.shape = (3, 4) -- (row列數,column行數)
print("Xdf1.head(2) =",Xdf1.head(2))         #-- 前數行(head)與後數行(tail)
# Xdf1.head(2) =          channel product  quantity  amount
#               customer                                  
#               c1            s1      p1         1    1200
#               c2            s2      p2         1     800
print("Xdf1.index=",Xdf1.index)      #-- Xdf1.index= Index(['c1', 'c2', 'c3'], dtype='object', name='customer')
print("Xdf1.columns=",Xdf1.columns)  #-- Xdf1.columns= Index(['channel', 'product', 'quantity', 'amount'], dtype='object')
Xdf2 = Xdf1.reset_index();    print(Xdf2)   #-- Xdf2 和 Xdf 相同

#%%##===== (D4) 數據框索引 =====#####
print(Xdf1)
##== (1).提取列與行
##--  (1a).提取列(row,index)
print("Xdf1.loc['c2']=",Xdf1.loc['c2'])   #-- (a1)提取指定索引的列 .loc['c2'] 
# Xdf1.loc['c2']= channel      s2
#                 product      p2
#                 quantity      1
#                 amount      800
# Name: c2, dtype: object
print("Xdf1.iloc[2]=",Xdf1.iloc[2])       #-- (a2)提取第 k(2)列: .iloc[2]
# Xdf1.iloc[2]= channel       s3
#               product       p3
#               quantity       2
#               amount      3200
# Name: c3, dtype: object
print("Xdf1[1:3]=",Xdf1[1:3])             #-- (a3)提取第1:3(1-2)列 (沒有第0列) 
#          channel product  quantity  amount
# customer                                  
# c2            s2      p2         1     800
# c3            s3      p3         2    3200
##-- (1b).提取行(column)
print("Xdf1['product']=",Xdf1['product'])         #-- (a)按照列名稱，提取指定的行
# Xdf1['product']= customer
#                       c1    p1
#                       c2    p2
#                       c3    p3
# Name: product, dtype: object

#%%== (2).提取元素
##--  (2a).提取 列行 元素(.values[])
print("Xdf.values[2]=",Xdf.values[2])         #-- [列] --> ['c3' 's3' 'p3' 2 3200]
print("Xdf.values[2][4]=",Xdf.values[2][4])   #-- [列][行] --> 3200
print("Xdf.values[2][4]=",Xdf.values[2][4])   #-- [列][行] --> 3200
#%%== (2b).條件式提取元素 (.loc[])
print("Xdf.loc[Xdf['amount']>3000] =",Xdf.loc[Xdf['amount']>3000])
# Xdf.loc[Xdf['amount']>3000] =   customer channel product  quantity  amount
#                               2       c3      s3      p3         2    3200
print("Xdf.loc[(Xdf['amount']<1000)|(Xdf['quantity']>=2)] =",Xdf.loc[(Xdf['amount']<1000)].loc[(Xdf['quantity']<=1)])
# Xdf.loc[(Xdf['amount']<1000)|(Xdf['quantity']>=2)] =   
#   customer channel product  quantity  amount
# 1       c2      s2      p2         1     800
# 2       c3      s3      p3         2    3200
# print("something =",Xdf.loc[(Xdf['amount']<1000)].loc[(Xdf['quantity']<=1)])
print("something =",Xdf.loc[(Xdf['amount']<1000)&(Xdf['quantity']<=1)])
print("something2 =",Xdf.loc[(Xdf['amount']<1000)].loc[(Xdf['quantity']<=1)])

#%%##===== (D5) 數據框的增減 =====#####
df4 = pd.DataFrame({"customer":["c4"], "channel":["s4"], "product":["p4"], "quantity":[3], "amount":[1500]})
Xdf4 = pd.concat([Xdf,df4]);   print("Xdf4 = ",Xdf4)
# Xdf4 =    customer channel product  quantity  amount
#         0       c1      s1      p1         1    1200
#         1       c2      s2      p2         1     800
#         2       c3      s3      p3         2    3200
#         0       c4      s4      p4         3    1500
Xdf4a = Xdf4.drop([0],axis=0);      print("Xdf4a = ",Xdf4a)
# Xdf4a =    customer channel product  quantity  amount   ---> 小心, 有2個index=0, 所以一次會刪掉2列
#          1       c2      s2      p2         1     800
#          2       c3      s3      p3         2    3200
Xdf4b = Xdf4a.drop(["quantity"],axis=1);      print("Xdf4b = ",Xdf4b)
# Xdf4b =    customer channel product  amount
#          1       c2      s2      p2     800
#          2       c3      s3      p3    3200

#%%##===== (D6) 讀取數據框 =====#####
XXX = pd.read_csv(wkDir+"XXX.csv");   print(XXX.shape);   print(XXX.head(2))   #-- (84008, 11)
#   invoiceNo channel customer product  ... quantity  amount category2    cost
# 0        N1      s1       c1      p1  ...        1    1692      sub1  931.39
# 1        N2      s1       c2      p2  ...        1    1197      sub2  793.36
##== 商品零售的標規檔
#    -- 商品零售: 將商品或服務(P, product)出售(S, channel)給最終消費者(C, customer)的全部活動。
#    -- 商品只有通過零售，才能真正實現其價值
#    -- 商品零售的模型: SPC模型 

#%%##===== [實作3] 您的數據，具有怎樣的模型呢? =====#####


#%%####### (E) 簡易式互動網站設計 (st) (1hr) ##########

#%%##===== (E1) streamlit介紹 [Wiki] =====#####
#== 以 python 開發機器學習與數據科學之 open-source 平台的軟體公司
#== 重要時程:
#   -- 1990: Adrien Treuille, Thiago Teixeira 與 Amanda Kelly 建立於1990
#   -- 2019: 自 Gradient Ventures 與 Bloomberg Beta 募得六百萬美金資金
#   -- 2020: 自 Gradient Ventures, GGV Capital, Bloomberg Beta, Daniel Gross 與 Elad Gil 加募得 兩千一百萬美金

#%%##===== (E2) streamlit安裝與測試 =====#####
# 在 Anaconda Powershell prompt中下安裝指令: > pip install streamlit
# 可以測試 是否安裝成功:                     > streamlit hello
# --> 可以在瀏覽器中，觀看網頁程式的互動結果: localhost:8501

#%%##===== (E3) streamlit基本程式撰寫 [*網站.py(E3)] =====#####
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)

#%%##===== (E4) 系統基本架構 [*網站.py(E4)] =====#####
##== (1).通常包括 -- 
#        -- sidebar(邊欄,控制盤): st.sidebar. title/head/控制項/顯示項
#        -- canvas(主畫布): st. title/head/顯示項(包括圖形)
#        -- navbar(導航列): (此處未包括)
##== (2).主畫布和控制盤的主標題(title)
st.title("台新銀行: 大數據實務")      #-- canvas
st.sidebar.title("控制盤")           #-- sidebar
##== (3).(KDD1) 交易數據擷取 (files-->XXX) =====#####
if st.sidebar.checkbox("(1) 擷取交易數據 (-->XXX)"):    #-- (3A) 由用戶於控制盤勾選後,再進行數據讀取
    print("\n\n>>>>> (1) 擷取交易數據 (-->XXX) -----")  #-- 偵錯用
    XXX = pd.read_csv(wkDir+"XXX.csv")                  ##== (D6) 讀取數據框
    st.sidebar.write("* 交易數據檔 = XXX.csv")          #-- (3B) 以下為 控制盤(sidebar)設計
    st.sidebar.write("* 交易記錄數 = ", XXX.shape[0])   
    st.header("(1) 擷取交易數據檔(-->XXX)")             #-- (3C) 以下為 主畫面(content)設計
    st.write("* 交易記錄數 = ", XXX.shape[0])  
    st.dataframe(XXX.head(3))

#%%##===== (E5) 網站執行方式 =====#####
##== (1) 儲存本程式
##== (2) 打開 Anaconda powershell prompt 進入系統控制台
##== (3) 切換目錄到本程式目錄
##== (4) 下指令 streamlit run 台新python01網站.py
##== (5).在瀏覽器中觀看程式: localhost:8501

#%%##===== [實作4] 安裝streamlit, 跑出您的第一個網站來… =====#####


#%%####### (F) 數據來源 (1hr) ##########

#%%##===== (F1) 內置數據集 =====#####

##== sklearn/datasets: 提供了一些數據生成器和數據加載工具, 共有24個數據集
from sklearn import datasets
iris = datasets.load_iris()
print(iris.feature_names)   #-- ['sepal length (cm)', 'sepal width (cm)', 'petal length (cm)', 'petal width (cm)']
print(iris.target_names)    #-- ['setosa' 'versicolor' 'virginica']
print(iris.data.shape)      #-- (150,4)
print(iris.data[0:2,])      #-- [[5.1 3.5 1.4 0.2] [4.9 3.  1.4 0.2]]

#%%##===== (F2) 企業數據 =====#####

##== (1).讀csv檔案
XXX = pd.read_csv(wkDir+"XXX.csv");   print(XXX.shape);    print(XXX.head(2))   #-- (84008, 11)
#   invoiceNo channel customer product  ... quantity  amount category2    cost
# 0        N1      s1       c1      p1  ...        1    1692      sub1  931.39
# 1        N2      s1       c2      p2  ...        1    1197      sub2  793.36
##== (2).寫xlsx檔案
XXX.to_excel("Xtest.xlsx")
##== (3).讀xlsx檔案
Xtest = pd.read_excel("Xtest.xlsx");    print(Xtest.shape);   print(Xtest.head(2))   #-- (84008, 12) -- 多了一個索引列
#    Unnamed: 0 invoiceNo channel customer  ... quantity amount  category2    cost
# 0           0        N1      s1       c1  ...        1   1692       sub1  931.39
# 1           1        N2      s1       c2  ...        1   1197       sub2  793.36

#%%##===== (F3) 雲端(網路)數據 =====#####

##== (1).requests: 可建立各種 HTTP 請求，從網頁伺服器上取得資料的軟件包
import requests
URL = "https://tw.stock.yahoo.com/quote/2330"   #-- yahoo 股市+台積電
response = requests.get(URL)

##== (2).BeautifulSoup: 網頁爬蟲的軟件包，可取回HTML網頁，解析HTML結構，取得所要的資料
from bs4 import BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")
print(soup.prettify()[0:400])       #-- 排版後的HTML內容
# '<!DOCTYPE html>\n<html class="NoJs desktop" id="atomic" lang="zh-Hant-TW">\n <head prefix="og: http://ogp.me/ns#">\n  
# <script>\n   window.performance && window.performance.mark && window.performance.mark(\'PageStart\');\n  </script>\n  
# <meta charset="utf-8"/>\n  <meta content="website" property="og:type"/>\n  
# <meta content="台積電(2330.TW)，Yahoo奇摩股市提供您即時報價、個股走勢、成交資訊、當日籌碼，價量變化、個股相關新聞等即時資訊。" property="og:descrip'
 

#%%##===== (F4).物聯(設備)+(F5).開放數據(open data) =====#####

##== (1).kaggle [wiki, kaggle]: 
#        -- 澳洲經濟學家Anthony Goldbloom 於2010/04在美國舊金山成立, 2017/03由google收購。
#        -- 是一個數據建模和數據分析競賽平台,可高達300萬美金,全球有近20萬名數據科學家參與
##== (2).Data Station: 自2021年開始,資策會建立之數據平台
##== (3).Data.Taipei臺北市政府資料大平臺: 2011/09上線
URL = 'https://tcgbusfs.blob.core.windows.net/blobyoubike/YouBikeTP.json'
response = requests.get(URL)
jsonData = response.json()
data = list(jsonData["retVal"].values());   
print(len(data));   print(data[0:2])   #-- 369
# [{'sno': '0001', 'sna': '捷運市政府站(3號出口)', 'tot': '84', 'sbi': '72', 'sarea': '信義區', 'mday': '20221030161036', 'lat': '25.0408578889', 'lng': '121.567904444', 'ar': '忠孝東路/松仁路(東南側)', 'sareaen': 'Xinyi Dist.', 'snaen': 'MRT Taipei City Hall Stataion(Exit 3)-2', 'aren': 'The S.W. side of Road Zhongxiao East Road & Road Chung Yan.', 'bemp': '12', 'act': '1'}, 
#  {'sno': '0002', 'sna': '捷運國父紀念館站(2號出口)', 'tot': '16', 'sbi': '3', 'sarea': '大安區', 'mday': '20221030161031', 'lat': '25.041254', 'lng': '121.55742', 'ar': '忠孝東路四段/光復南路口(西南側)', 'sareaen': 'Daan Dist.', 'snaen': 'MRT S.Y.S Memorial Hall Stataion(Exit 2.)', 'aren': 'Sec,4. Zhongxiao E.Rd/GuangFu S. Rd', 'bemp': '13', 'act': '1'}]

#%%##===== [實作5] 您的數據，屬於哪一類呢? =====#####


#%%####### (G) 數據分析系統 (1hr) ##########

#%%##===== (G1) 大數據分析(Big Data Analysis, BDA) =====#####
##== (1).數據分析的標準步驟：知識發現(KDD, Knowledge Discovery in Databases) [Fayyad et al., 1996]
##== (2).KDD步驟: 
#        -- (KDD1) 數據擷取(Data Acquisition)
#                  --> 當熟練後, 這部份最花時間，約需一半以上的時間
#        -- (KDD2) 數據處理(Data Processing): 一般 包括 數據清理、數據整合、數據轉換、數據化約
#                  --> 前兩者 (數據清理與數據整合) -- 融入 (KDD1)數據擷取, 為數據前處理(Pre-processing)
#                  --> 後兩者 (數據轉換與化約)     -- 通常在(KDD3)數據轉換 進行, 一般儘量不做化約(reduction)
#                  --> 實務上，將 KDD2 改為 數據探索(Data Exploration), 進行數據空間分析
#        -- (KDD3) 數據轉換(Data Transformation)
#                  --> 數據分析的核心，用以產生標籤(tag)
#        -- (KDD4) 數據模型(Data Modeling)，是數據分析的牛肉, 包括
#                  --> <1> 一維圖形呈現: 折線圖, 長條圖, 橫條圖, 圓餅圖, 散布圖, ...
#                  --> <2> OLAP (OnLine Analytic Processing, 在線分析處理, Power BI) 的 多維度分析(MDA, Multi-Dimensional Analysis) 
#                  --> <3> 數據探勘(Data Mining): 數據聚類(Clustering), 數據關連(Association), 數據序列(Sequencing)
#                  --> <4> 人工智能(AI切入點)/機器學習(Machine Learning): 預測(Prediction),決策(Decision),分類(Classification)
#        -- (KDD5) 數據解讀(Data Interpretation): 數據分析的亮點，要對模型進行洞察(insight)
#                  --> 結合數據視覺化(Visualization)，才能表現數據的價值，現在已以數位儀表板(dashboard)方式呈現
##== (3).KDD成果呈現方式
#        -- <1> 報告: Powerpoint, Word, PDF, Excel
#        -- <2> 表單: Excel
#        -- <3> 儀表板: Power BI, python, R/shiny
#        -- <4> 互動網站: Power Bi, python
#        -- <5> 機器人: 未來的 chatGPT

#%%##===== (G2) 數據分析練習1: 交易週時模型  =====#####
##== (1).(KDD3) 產生週/時標籤 (hour,weekday)
XXX["hour"] = pd.to_datetime(XXX["datetime"]).dt.hour          #-- 還有很多其他產生此標籤的方法, 這裡只是取其中較方便的一種
XXX["weekday"] = pd.to_datetime(XXX["datetime"]).dt.weekday    #-- 0 表示週一, 1 表示週二, ...
##== (2).(KDD4) 建立 交易週時模型 (TTT)
TTT = pd.crosstab( XXX["hour"], XXX["weekday"], margins=True );   print(TTT[0:3])
# weekday    0    1    2    3    4    5    6   All
# hour                                            
# 0          0    2    0    0    0    0    0     2
# 10         5    2    5    2    2    1    4    21
# 11       175  137  163  148  135  227  338  1323
#%%##===== (G3) 交易週時模型加入互動系統 (hour,weekday) [*網站.py(G3)] =====#####
if st.sidebar.checkbox("(2) 產生交易週時模型"):       #-- (A) 由用戶於控制盤勾選後,再進行數據讀取
    print("\n\n>>>>> (2) 產生交易週時模型 -----")     #-- 偵錯用 
    XXX["hour"] = pd.to_datetime(XXX["datetime"]).dt.hour           ##== (G2-1).(KDD3) 產生週/時標籤 (hour,weekday)
    XXX["weekday"] = pd.to_datetime(XXX["datetime"]).dt.weekday    
    TTT = pd.crosstab( XXX["hour"], XXX["weekday"], margins=True ); print(TTT[0:3])  ##== (G2-2).(KDD4) 建立 交易週時模型 (TTT)
    st.header("(2) 交易週時模型(XXX[hour,weekday])")  #-- (B) 以下為 主畫面(canvas)設計
    st.write("(2A) (KDD3) 產生的數據標籤-- ")  
    st.dataframe(XXX.head(3))
    st.write("(2B) (KDD4) 交易週時模型-- ")  
    st.dataframe(TTT)   

#%%##===== [實作6] 回去架個您自己的網站厚!! =====#####

