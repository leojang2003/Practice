# 台新python01網站.py: Python Web - 01: Introduction, Platform and Basics
# Jia-Sheng Heh, 07/20/2023, revised from AIp1101.py
# Usage: streamlit run 台新python01網站.py

#%%##===== (C1).設定工作目錄 =====#####
import os     #==> 任何數據分析編程的第一件事：設定工作目錄(Working Directory)
wkDir = "c:/Users/jsheh/Desktop/newWorking/Consult/Yago台新--Python基礎班202308/";   os.chdir(wkDir)
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
    TTT = pd.crosstab( XXX["hour"], XXX["weekday"], margins=True ); print(TTT[0:3])  ##== (G2-2).(KDD4) 建立 交易週時模型 (TTT)
    st.header("(2) 交易週時模型(XXX[hour,weekday])")  #-- (B) 以下為 主畫面(content)設計
    st.write("(2A) (KDD3) 產生的數據標籤-- ")  
    st.dataframe(XXX.head(3))
    st.write("(2B) (KDD4) 交易週時模型-- ")  
    st.dataframe(TTT)   

