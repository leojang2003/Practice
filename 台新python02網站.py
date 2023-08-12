# 台新python01網站.py: Python Web - 01: Introduction, Platform and Basics
# Jia-Sheng Heh, 07/20/2023, revised from AIp1101.py
# Usage: streamlit run 台新python02網站.py

#%%##===== (C1).設定工作目錄 =====#####
import os     #==> 任何數據分析編程的第一件事：設定工作目錄(Working Directory)
wkDir = "c:/Users/jsheh/Desktop/newWorking/Consult/Yago台新--Python基礎班202308/day2/";   os.chdir(wkDir)
print(os.getcwd())
###>> [實作演練] 花點時間，修改上述目錄名稱為，你儲存本程式 (台新python01網站.py) 的目錄
# 注意: Windows的路徑，複製過來時，會是反斜線(backslash,\)，要改成正斜線(slash,/)

#%%##===== (D6) (KDD1) 讀取數據框 =====#####
import pandas as pd
XXX = pd.read_csv(wkDir+"XXX.csv");   print(XXX.shape);   print(XXX.head(2))   #-- (84008, 11)
#   invoiceNo channel customer product  ... quantity  amount category2    cost
# 0        N1      s1       c1      p1  ...        1    1692      sub1  931.39
# 1        N2      s1       c2      p2  ...        1    1197      sub2  793.36

#%%##===== (E3) streamlit基本程式撰寫 =====#####
import streamlit as st
st.set_option('deprecation.showPyplotGlobalUse', False)

#%%##===== (E4) 系統基本架構 =====#####
##== (1).通常包括 -- 
#        -- sidebar(邊欄,控制盤): st.sidebar. title/head/控制項/顯示項
#        -- canvas(主畫布): st. title/head/顯示項(包括圖形)
#        -- navbar(導航列): (此處未包括)
##== (2).主畫布和控制盤的主標題(title)
st.title("台新銀行: 大數據實務網站")      #-- canvas
st.sidebar.title("控制盤")               #-- sidebar
##== (3).(KDD1) 交易數據擷取 (files-->XXX) =====#####
if st.sidebar.checkbox("(1) 擷取交易數據 (-->XXX)"):    #-- (3A) 由用戶於控制盤勾選後,再進行數據讀取
    print("\n\n>>>>> (1) 擷取交易數據 (-->XXX) -----")  #-- 偵錯用
    XXX = pd.read_csv(wkDir+"XXX.csv")                  ##== (D6) 讀取數據框
    st.sidebar.write("* 交易數據檔 = XXX.csv")          #-- (3B) 以下為 控制盤(sidebar)設計
    st.sidebar.write("* 交易記錄數 = ", XXX.shape[0])   
    st.header("(1) 擷取交易數據檔(-->XXX)")             #-- (3B) 以下為 主畫面(content)設計
    st.write("* 交易記錄數 = ", XXX.shape[0])  
    st.dataframe(XXX.head(3))

#%%##===== (G3) 交易週時模型加入互動系統 (hour,weekday) [*網站.py(G3)] =====#####
if st.sidebar.checkbox("(2) 產生交易週時模型"):       #-- (A) 由用戶於控制盤勾選後,再進行數據讀取
    print("\n\n>>>>> (2) 產生交易週時模型 -----")     #-- 偵錯用 
    XXX["hour"] = pd.to_datetime(XXX["datetime"]).dt.hour           ##== (G2-1).(KDD3) 產生週/時標籤 (hour,weekday)
    XXX["weekday"] = pd.to_datetime(XXX["datetime"]).dt.weekday    
    TTThw = pd.crosstab( XXX["hour"], XXX["weekday"], margins=True ); print(TTThw[0:3])  ##== (G2-2).(KDD4) 建立 交易週時模型 (TTT)
    st.header("(2) 交易週時模型(XXX[hour,weekday])")  #-- (B) 以下為 主畫面(content)設計
    st.write("(2A) (KDD3) 產生的數據標籤-- ")  
    st.dataframe(XXX.head(3))
    st.write("(2B) (KDD4) 交易週時模型-- ")  
    st.dataframe(TTThw)   


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
 

#%%##===== (2C1) (KDD3) 轉換客戶數據框加入互動系統入 (Cv+FF0+MM0) [*網站2.py(2C1)] =====#####
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
