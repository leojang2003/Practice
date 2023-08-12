# 台新python02教學AM.py: Python Practices - 02AM (A-C) for 台新銀行
# Jia-Sheng Heh, 07/23/2023, revised from 台新python01A_環境與numpy.py

import os   
wkDir = "c:/Users/Admin/Desktop/台新python/";   os.chdir(wkDir)
print(os.getcwd())
import numpy as np
import pandas as pd
# import streamlit as st   #--> 好像會和 plotly.express 相色衝, 使得繪圖沒有彩色 (3D)

#%%####### (2A) 數據空間與數據轉換 (1hr) ##########

#%%##===== (D6-->2A1) 讀取數據框 (file-->XXX) =====#####
XXX = pd.read_csv(wkDir+"XXX.csv")
XXX["date"] = pd.to_datetime(XXX["datetime"]).dt.date   #-- 還有很多其他產生此標籤的方法, 這裡只是取其中較方便的一種
print(XXX.shape)
print(XXX.head(2))  # -- (84008, 12)
#   invoiceNo channel customer product  ... amount  category2    cost        date
# 0        N1      s1       c1      p1  ...   1692       sub1  931.39  2015-01-07
# 1        N2      s1       c2      p2  ...   1197       sub2  793.36  2015-01-18

#%%##===== (2A2) 數據空間 =====#####
##== (1).數據的維度(dimension)/軸向(axis): 收攏相關屬性，並具有索引鍵(key)
##== (2).可以進行數據空間分解 -- SPC模型的維度: 在 S通路銷售 P商品 給 C客戶
#        -- S (銷售): 通路—店舖—銷售者 ====================---> 通路銷售(動詞) 
#        -- P (商品): 品牌—品類—品項 ======================---> 商品 (受詞)
#        -- C (客戶): 會員/非會員—客層(客戶價值)—客群—客戶 =---> 客戶 (主詞)
#        -- T (時間): 年—季—月—週—日—時
print(XXX.iloc[0])
# channel                       s1 ===--> S維度 (通路銷售) 
# customer                      c1 ===--> C維度 (客戶)
# product                       p1 ===--> P維度 (商品)
# category                   kind1 ===------P的上階層維度
# category2                   sub1 ===------P的次上階層屬性
# price                       1980 ===------P的價格屬性
# cost                      931.39 ===------P的成本屬性
# datetime     2015-01-07 20:07:11 ===--> T維度
# invoiceNo                     N1 ===------T維度相關的順序
# date                  2015-01-07 ===------T維度的計算
# quantity                       1
# amount                      1692

#%%##===== (2A3) 數據空間的視覺化 =====#####
##== (1).plotly: open-source科學圖形函式庫，能做到視覺化互動報表  
#        -- 在終端機中 pip install plotly 安裝 
import plotly.express as px     #-- Plotly Express: Plotly的高级封装，以容易地進行數據框的圖表
import plotly.io as pio         #-- plotly 以網頁型式呈現, 可表現出 hovering的效果
pio.renderers.default = 'browser'
##== (2).SPC模型的3D圖示
df = XXX.iloc[0:20][["channel","customer","product","date","amount"]]
print(df.head(2))
#   channel customer product        date  amount
# 0      s1       c1      p1  2015-01-07    1692
# 1      s1       c2      p2  2015-01-18    1197
fig = px.scatter_3d(df, x='customer', y='product', z='channel', color='customer')  #-- 散點(scatter)圖: 點,線,或 點+線
fig.show()
##== (3).數據空間的應用: 可切割為若干狀態，並進行狀態切換等數據關連操作

#%%##===== (2A4) 數據分析+繪圖: 產生各通路營業額趨勢圖 =====#####
##== (1).(KDD3) 產生年度(year)標籤
XXX["year"] = pd.to_datetime(XXX["datetime"]).dt.year    #-- 還有很多其他產生此標籤的方法, 這裡只是取其中較方便的一種      
##== (2).(KDD3) 空間轉換產生通路年度(channel--year)數據框--> 下次再細講
Sv = XXX.groupby(["year","channel"]).agg({"amount":"sum"}).reset_index();
print(Sv.shape);   print(Sv.head(4))   #-- (15, 3)
#   channel  year    amount
# 0      s1  2015   4822236
# 1      s1  2016   6670402
# 2      s1  2017  11142368
# 3      s2  2015  12474878
##== (3).(KDD4) 繪出 各通路營業額趨勢圖
fig = px.line(Sv, x="year", y="amount", color="channel")  #-- 線性圖(line chart)
fig.update_traces(textposition="bottom right")
fig.show()

#%%##===== (2A5) 各通路營業額趨勢圖加入互動系統 (year,Sv) [*網站.py(G5)] =====#####
if st.sidebar.checkbox("(3) 產生各通路營業額趨勢圖"):    #-- (A) 由用戶於控制盤勾選後,再進行數據讀取
    print("\n\n>>>>> (3) 產生各通路營業額趨勢圖 -----")      #-- 偵錯用
    XXX["year"] = pd.to_datetime(XXX["datetime"]).dt.year   ##== (2A4-1).(KDD3) 產生年度(year)標籤      
    Sv = XXX.groupby(["year","channel"]).agg({"amount":"sum"}).reset_index();
                                                            ##== (2A4-2).(KDD3) 空間轉換產生通路年度(Sv)數據框
    import plotly.express as px                             ##== (2A3-1).調用plotly科學圖形函式庫
    # import plotly.io as pio         #-- plotly 以網頁型式呈現, 可表現出 hovering的效果
    fig = px.line(Sv, x="year", y="amount", color="channel", text="amount")
    fig.update_traces(textposition="bottom right")          ##== (2A4-3).(KDD4) 繪出 各通路營業額趨勢圖
    st.header("(3) 各通路營業額趨勢圖")                  #-- (B) 以下為 主畫面(canvas)設計
    st.write("(3A) (KDD3) 產生的XXX數據標籤-- ")  
    st.dataframe(XXX.head(3))
    st.write("(3B) (KDD3) 產生的Sv數據-- ")  
    st.dataframe(Sv.head(3))
    st.write("(3C) (KDD4) 各通路營業額趨勢圖-- ")  
    st.plotly_chart(fig)

#%%##===== [實作2-1] 請用streamlit跑出上述程式，如果可以的話，加個您自己的圖形 =====#####

#%%####### (2B) 客戶價值模型 (1hr) ##########

#%%##===== (2B1) (KDD3) 數據轉換: 數據框轉換/樞紐(pivot)轉換 (XXX-->Cv) =====#####
##== SPC轉換: 在數據空間中，從交易數據(X), 投射到某特定軸 (S軸/P軸/C軸) 的轉換，可以產生此軸上的新數據集
#    -- 如: (2A4)是投射到 S軸 (+年份year) 的 通路導向樞紐轉換,
#       而此處是 投射到 C軸上的 客戶導向樞紐轉換
XXX["date"] = pd.to_datetime(XXX["datetime"]).dt.date   ##== (2B1-1).(KDD3) 產生日期(date)標籤      
Cv = XXX.groupby("customer").agg({"invoiceNo":"nunique", "amount":"sum", "quantity":"sum",
                                  "date":["min","max"],
                             })                         ##== (2B1-2).(KDD3) 產生客戶價值(Cv)標籤
Cv.columns = ["FF","MM","TT", "D0","Df"]
print(Cv.shape);   print(Cv.head(2))   #-- (7774, 5)
#           FF      MM     TT           D0          Df
# customer                                      
# c1         1    3335      3   2015-01-07  2015-01-07
# c10        1    2770      1   2015-01-28  2015-01-28
#     造訪頻次 購買金額 購買件數  首次造訪日  最近造訪日
#%%##===== (2B2) 客戶價值模型: RFM模型 =====#####
##== 客戶分層: 區隔不同價值的顧客 [Arthur Hughes, 1994] [Stone, 1989]
##== RFM模型 [Miglautsch, 2000]
#    -- (1).顧客最近的消費/購買時間 (Recency,R): --> D0 (首次造訪日), Df (最後造訪日)
#           -- 即顧客最近一次購買的時間與現在時間的距離天數
#           -- 用來衡量顧客再次購買的可能性。時間距離愈近則再次購買程度愈高
#    -- (2).造訪頻次(Frequency,F)---量: 客戶"腳"的行為 --> FF (常客)
#           -- 在某段期間內購買該企業產品的總次數，此期間可定義為一個月、一季或任何時間長度
#           -- 用來衡量顧客在購買行為中與企業的互動程度，頻率愈高表示顧客的熱衷程度愈高。
#    -- (3).購買金額(Monetary,M)---質: 客戶"手"的行為 --> MM (貴客)
#           -- 在某段期間內購買該企業產品的總金額，
#           -- 用來評價顧客對該企業的貢獻度及顧客價值。金額愈高表示價值較高

#%%##===== (2B3) (KDD3) 數據離散化 (FF,MM-->FF0,MM0) 到 客戶圖像(Customer Profile) =====#####
##== pd.cut: 切分(segment)數據 
Cv["FF0"] = pd.cut(Cv["FF"], bins=[0,1,9,99,999,19999]).astype(str)  
Cv["MM0"] = pd.cut(Cv["MM"], bins=[-5000,0,999,9999,99999,999999,19999999]).astype(str)
print(Cv.shape);   print(Cv.head(2))   #-- (7774, 7)
#           FF    MM  TT          D0          Df     FF0          MM0
# customer                                                           
# c1         1  3335   3  2015-01-07  2015-01-07  (0, 1]  (999, 9999]
# c10        1  2770   1  2015-01-28  2015-01-28  (0, 1]  (999, 9999]
##== 這是一種 客戶圖像(customer profile) --
#    -- (1).本質(behavior)變量:    關於年齡,性別,身高,體重,學歷,經歷等資料, 常與個資有關
#    -- (2).傾向(inclination)變量: 關於顏色,尺寸,風格,商品性能等喜好或傾向, 常以問卷進行收集
#    -- (3).行為(behavior)變量:    關於造訪,購買,使用,選擇等行為的紀錄, 常為擷取數據的內容 
#           ----> FF: 腳的行為(造訪), MM: 手的行為(購買)
### Cv.to_csv("Cv.csv")
#%%##===== (2B4) (KDD4) 客戶價值模型 (Cv['FF0','MM0']) =====#####
##== (1).表格(pd.crosstab())是最常見,也最有用的模型
##== (2).客戶價值(customer value)
#        -- 顧客對於給予和獲取的主觀感知態度, 影響消費者對產品的整體評價 (Zang, 2022)
#        -- 客戶價值模型: 表現 每位客戶的 質(quality,MM0) 與 量(quantity,FF) 的模型
TFM = pd.crosstab(Cv["FF0"], Cv["MM0"], margins=True)   
print(TFM)
# MM0           (-5000, 0]  (0, 999]  ...  (999999, 19999999]   All
# FF0                                 ...                          
# (0, 1]                14       901  ...                   0  4169
# (1, 9]                 6        36  ...                   0  3225
# (9, 99]                0         0  ...                   0   368
# (99, 999]              0         0  ...                   0     8
# (999, 19999]           0         0  ...                   4     4
# All                   20       937  ...                   4  7774
TFM.to_csv("TFM.csv")
#%%##===== (2B5) (KDD5) 客戶價值模型的解讀 (Cv['FF0','MM0']) =====#####
print("--(1) 一次客共",TFM["All"][0],"位。")           #-- (1).數據解讀,用來呈現數據分析的亮點(insight)
print("--(2) 數次客近",TFM["All"][1],"位，可深耕。")    #-- (2).在 python/R中,才有機會進行智能性的解讀
print("--(3) 超過十次的千元以上客，應做進一步分析，並可深入做VIP方案。")
print("--(4) 超過千次的異常客，應為非會員，應做進一步分析。")
# --(1) 一次客共 4169 位。
# --(2) 數次客近 3225 位，可深耕。
# --(3) 超過十次的千元以上客，應做進一步分析，並可深入做VIP方案。
# --(4) 超過千次的異常客，應為非會員，應做進一步分析。

#%%##===== [實作2-2] 您的實驗數據，能轉換出怎樣的數據框呢?又有機會建立怎樣的模型呢? =====#####

#%%####### (2C) 客戶價值模型 加入互動系統 (1hr) ##########

#%%##===== (2C1) (KDD3) 轉換客戶數據框加入互動系統 (Cv+FF0+MM0) [*網站2.py(2C1)] =====#####
if st.sidebar.checkbox("(4) (KDD3) 轉換客戶圖像(數據框) (XXX-->Cv)"):   
    print("\n\n>>>>> (4) (KDD3) 轉換客戶圖像 (-->XXX) -----")  #-- 偵錯用
    XXX["date"] = pd.to_datetime(XXX["datetime"]).dt.date   ##== (2B1-1).(KDD3) 產生日期(date)標籤      
    Cv = XXX.groupby("customer").agg({"invoiceNo":"nunique", "amount":"sum", "quantity":"sum",
                                      "date":["min","max"],
                                 })                         
    Cv.columns = ["FF","MM","TT", "D0","Df"]   ##== (2B1-2) (KDD3) 數據轉換: 數據框轉換/樞紐(pivot)轉換 (XXX-->Cv)
    Cv["FF0"] = pd.cut(Cv["FF"], bins=[0,1,9,99,999,19999]).astype(str)  
    Cv["MM0"] = pd.cut(Cv["MM"], bins=[-5000,0,999,9999,99999,999999,19999999]).astype(str)
                                               ##== (2B3) (KDD3) 數據離散化 (FF,MM-->FF0,MM0)
    st.sidebar.write("* 客戶數 = ", Cv.shape[0])   
    st.header("(4) 轉換出客戶圖像,並離散化(XXX-->Cv)")     
    st.dataframe(Cv.head(3))

#%%##===== (2C2) (KDD4) 客戶價值模型加入互動系統 (Cv['FF0','MM0']) [*網站2.py(2C2)] =====#####
if st.sidebar.checkbox("(5) (KDD4) 客戶價值模型 (Cv['FF0','MM0'])"):
    TFM = pd.crosstab(Cv["FF0"], Cv["MM0"], margins=True)   ##== (2B4) (KDD4) 客戶價值模型 (Cv['FF0','MM0'])
    st.header("(5)  (KDD4) 客戶價值模型 (Cv['FF0','MM0']) --")
    st.write("* 以 客戶的造訪頻次(FF0) 與 客戶的消費金額(MM0) 形成 客戶價值模型：")
    st.dataframe(TFM)
    
#%%##===== (2C3) (KDD5) 數據解讀 加入互動系統 (Cv['FF0','MM0']) [*網站2.py(2C3)] =====#####
if st.sidebar.checkbox("(6) (KDD5) 解讀 客戶價值模型 --"):       
    st.header("(6)  (KDD5) 解讀客戶價值模型 --")
    st.write("--<1> 一次客共",TFM["All"][0],"位。")          ##== (2B5) (KDD5) 客戶價值模型的解讀 (Cv['FF0','MM0'])
    st.write("--<2> 數次客近",TFM["All"][1],"位，可深耕。")
    st.write("--<3> 超過十次的千元以上客，應做進一步分析，並可深入做VIP方案。")
    st.write("--<4> 超過千次的異常客，應為非會員，應做進一步分析。")

#%%##===== [實作2-3] 展示一下您上次回去做的系統，看看有沒有機會加入數據轉換… =====#####

