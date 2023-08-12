# 台新python02教學PM.py: Python Practices - 02PM (D-F) for 台新銀行
# Jia-Sheng Heh, 07/23/2023, revised from 台新python01A_環境與numpy.py

import os   
wkDir = "c:/Users/jsheh/Desktop/newWorking/Consult/Yago台新--Python基礎班202308/day2/";   os.chdir(wkDir)
print(os.getcwd())
import numpy as np
import pandas as pd

#%%####### (2D) 數據標籤回射 (Cv-->XXX) (1hr) ##########

#%%##===== (2D1/2A1) 讀取數據框 (file-->XXX) =====#####
XXX = pd.read_csv(wkDir+"XXX.csv");    
XXX["date"] = pd.to_datetime(XXX["datetime"]).dt.date
print(XXX.shape);   print(XXX.head(2))   #-- (84008, 12)
#   invoiceNo channel customer product  ... amount  category2    cost        date
# 0        N1      s1       c1      p1  ...   1692       sub1  931.39  2015-01-07
# 1        N2      s1       c2      p2  ...   1197       sub2  793.36  2015-01-18

#%%##===== (2D2/2B1) (KDD3) 數據轉換: 數據框轉換/樞紐(pivot)轉換 (XXX-->Cv) =====#####
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

#%%##===== (2D3/2B3) (KDD3) 數據離散化 (FF,MM-->FF0,MM0) =====#####
##== pd.cut: 切分(segment)數據 
Cv["FF0"] = pd.cut(Cv["FF"], bins=[0,1,9,99,999,19999]).astype(str)  
Cv["MM0"] = pd.cut(Cv["MM"], bins=[-5000,0,999,9999,99999,999999,19999999]).astype(str)
print(Cv.shape);   print(Cv.head(2))   #-- (7774, 7)
#           FF    MM  TT          D0          Df     FF0          MM0
# customer                                                           
# c1         1  3335   3  2015-01-07  2015-01-07  (0, 1]  (999, 9999]
# c10        1  2770   1  2015-01-28  2015-01-28  (0, 1]  (999, 9999]

#%%##===== (2D4/2B4) (KDD4) 客戶價值模型 (Cv['FF0','MM0']) =====#####
TFM = pd.crosstab(Cv["FF0"], Cv["MM0"], margins=True)   
print(TFM)
# MM0           (-5000, 0]  (0, 999]  ...  (999999, 19999999]   All
# FF0                                 ...                          
# (0, 1]                14       901  ...                   0  4169 <-- 一次客
# (1, 9]                 6        36  ...                   0  3225 <-- 數次客
# (9, 99]                0         0  ...                   0   368  <========== 消費十數次的常客
# (99, 999]              0         0  ...                   0     8  <========== 消費十數次的超常客
# (999, 19999]           0         0  ...                   4     4 <-- 異常的千次客(應該是非會員)
# All                   20       937  ...                   4  7774
##== 一次客/數次客的消費,均未成熟,有些分析要 針對 成熟的客群 (常客+超常客) 來進行 -- 如: 成熟客的消費類型(消費基因)
##== 這些分析, 多在原始的交易數據上進行

#%%##===== (2D5) (KDD3) 標籤回射 (Cv-->XXX) =====#####
##== Cv-->XXX: 將 Cv的 FF0,MM0, 回射到 XXX交易數據框上
XXX["CvFF0"] = [ Cv["FF0"][x] if x in Cv.index else None for x in XXX["customer"] ]
XXX["CvMM0"] = [ Cv["MM0"][x] if x in Cv.index else None for x in XXX["customer"] ]
print(XXX.head(2))
#   invoiceNo channel customer  ...         CvFF0               CvMM0   cat7
# 0        N1      s1       c1  ...        (0, 1]         (999, 9999]  kind1
# 1        N2      s1       c2  ...  (999, 19999]  (999999, 19999999]  kind1
print(XXX.iloc[10000])
# invoiceNo                  N4669
# channel                       s3
# customer                    c303
# product                     p918
# category                   kind1
# price                       1080
# datetime     2015-05-04 13:03:55
# quantity                       1
# amount                       681  <-- 本次消費金額
# category2                   sub1
# cost                      507.64
# date                  2015-05-04
# year                        2015
# CvFF0                    (9, 99]  <-- 從 Cv回射的標籤: 是 c303全部的 造訪頻次區間(FF0)
# CvMM0              (9999, 99999]  <-- 從 Cv回射的標籤: 是 c303全部的 消費金額區間(MM0)
##== 回射的目的: 是要在 XXX上, 進行 AI的若干操作 (聚類與決策)

#%%##===== (2D6) 選取部份交易數據 (XXX--(CvFF0,CvMM0)-->XXXFM) =====#####
##== 常貴客: 是 常客 與(and) 貴客(數萬元客)/超貴客(數十萬元客)
print(TFM[TFM.columns[3:5]])
# MM0           (9999, 99999]  (99999, 999999]
# FF0                                         
# (0, 1]                   35                0
# (1, 9]                  816                0
# (9, 99]                 342               25
# (99, 999]                 0                8
# (999, 19999]              0                0
# All                    1193               33)
ind = [(XXX["CvFF0"][k] in ["(9, 99]","(99, 999] "]) and (XXX["CvMM0"][k] in ["(9999, 99999]","(99999, 999999]"]) for k in np.arange(XXX.shape[0])]
XXXFM = XXX[ind];   print(XXXFM.shape);   print(XXXFM["customer"].nunique())   #-- (16746, 15),   367
#-->  367位常貴客, 即有 16746 筆交易

#%%##===== (2D7) 濃縮 數據欄位 的 數據種類 (category-->cat7) =====#####
CpM0 = pd.crosstab(XXXFM["customer"],XXXFM["category"]);   print(CpM0.shape)     #-- (367, 53) --> 原(category)有53種品類
sorted(list(CpM0.sum()),reverse=True)[0:10]  #-- [5860, 3739, 1513, 1467, 886, 829, 603;  310, 212, 163] --> 前7種品類(cat7)佔大多數
cat7 = list(CpM0.sum().index[CpM0.sum()>600]);   print(cat7)  #-- ['kind1', 'kind11', 'kind12', 'kind16', 'kind17', 'kind2', 'kind3']
XXXFM["cat7"] = [ gg if (gg in cat7) else "others" for gg in XXXFM["category"] ] #--> 將category濃縮為前七項cat7, 其他為 others
print(XXXFM.iloc[7502:7504])
#       invoiceNo channel customer product  ...  year    CvFF0          CvMM0    cat7
# 25777    N11792      s4    c2997   p1965  ...  2016  (9, 99]  (9999, 99999]  others
# 25785    N11767      s4     c372    p212  ...  2016  (9, 99]  (9999, 99999]  kind11

#%%##===== [實作2-4] 就您上次回去做的系統， 要加入AI，需要怎樣的數據欄位? =====#####

#%%####### (2E) 從大數據到 AI (0.5hr) ##########

#%%##===== (2E1) AI模型/系統(Model/System, M) =====#####

##== (1).系統/模型(System/Model, M): 輸出y = M( 輸入u )
##== (2).操作程序：AI是數據分析的第四階段(KDD4) 
#        -- (A) 訓練階段(Learning/Modeling/Estimation/Training Phase): (u, y) -> M#
#               ---- 由輸入/輸出 u與y，求取(估測estimate)模型M#
#        -- (B) 預測階段(Prediction/Production/Application Phase): (u_new, M#) -> y_predict
#               ---- 以所估測的模型M#與新的輸入 u_new，求取(估測)新的輸出 y_predict

#%%##===== (2E2) 商業智慧(Business Intelligence):數據分析以實現商業價值 =====#####
 
##== (1).SQL query: 數據庫查詢指令
#    -- (1A).數據庫基本操作: 增加(insert), 修改(modify), 刪除(delete)
#    -- (1B).數據庫查詢操作:選擇(select)…
##== (2).在線分析OLAP (On-Line Analysis Processing), 多維度分析(MDA, Multidemnsional Data Analysis)
#    -- 以方格(cube), 階層(hierarchy)等維度視角來分析數據
#    -- (2A).統計圖形: 折線圖, 圓形圖, 長條圖等等
#    -- (2B).表格
#    -- (2C).儀表板功能: 篩選, 設計標籤, 數據轉換…
##== (3).機器學習 (machine learning): 輸入數據(x,y)，可以學習得知識(規則,模型M#)  
##==   (3-1).非監督式學習 (Unsupervised learning)
#          == 無輸出y, 目標在於發掘輸入(u)的隱含特徵 --> 數據挖掘(Data Mining): 分為三種 --
#          -- (3-1A)聚類(clustering):           計算數據u的相似度，以產生其分類 ===> 本單元(F)簡易說明
#          -- (3-1B)關連規則(association rule): 計算多數據(ui-uj)間的關連。      
#          -- (3-1C)數據序列(data sequencing):  計算多數據(ui-uj-uk)間的時序關係。 
##==   (3-2).監督式學習 (Supervised learning)
#          == 具範例(u,y), y為教師(teacher, desired output) y, 以求得y=M(u)
#          -- (3-2-1)分類(classification): y 為離散數據 --> 決策樹(符號AI)，神經網絡(數值AI) ===> 下一單元(G)說明
#          -- (3-2-2)迴歸(regression): y 為連續數據 -- 統計與機率 的最後重點
#              --> 神經網路(neural network): 自 2014年後，進入深度學習(deep learning)
#              --> 所以，現在的 AI，是機器學習／大數據分析的一環 *** 


#%%####### (2F) 數據聚類 (Data Clustering) (1hr) ##########

#%%##===== (2F1) 數據的向量化(vectorization) (XXXFM-->CpM) =====#####
CpM = pd.crosstab(XXXFM["customer"],XXXFM["cat7"]);   
print(CpM.shape);   print(CpM.head(2))   #-- (367, 8)
# cat7      kind1  kind11  kind12  kind16  kind17  kind2  kind3  others
# customer                                                             
# c1017        17       2       1       0       0     11      1       3 
# c1049         1       0       0       8       4     12      0       1
##--> 每位客戶被特徵化(characterize)/向量化(vectorize) 為一個購買品類的向量

#%%##===== (2F2) 數據聚類(clustering) (CpM: linkage-->(dendrogram)-->fcluster: Cgroup) =====#####
##== scipy: 科學、工程的運算處理的軟件包
#           包含統計、最佳化化、整合、線性代數、傅立葉轉換圖像等科學運算
from scipy.cluster.hierarchy import linkage, fcluster, dendrogram
Z = linkage(CpM, metric="euclidean", method="ward")   ##== 階層式聚類(hierarchical clustering)
##== metric: 點之間的距離量度 -- euclidean, manhattan, hamming, cosine, ...
##== method: 群之間的距離計算方法 -- single, complete, average, centroid, ward, ... 
##== dendrogram (蟹爪圖, 樹圖) --> bottom-up 的 逐點聚類
#    -- 500點以下方易觀察, 用來決定聚類的數目 (此處看出 聚類數可取為 9)

#%%##===== (2F3) 聚類的類別(cluster) (CpM-->...-->Cgroup) =====#####
Cgroup = fcluster(Z, 9, criterion="maxclust")
print(Cgroup[0:30])  #-- [5 9 5 5 9 9 5 8 5 2 9 8 9 5 8 2 9 9 8 2 9 9 9 9 9 9 9 2 5 2]
pd.DataFrame(Cgroup).value_counts()
# 9    133 ---> (1).general group: 分不開的類(cluster)
# 5     97   ====> (3).其中的五個類(5,8,7,4,6), 具有較明顯的特徵
# 8     77
# 2     25
# 7     15
# 4     12   ====>
# 6      5 ---> (2).離異點(outliers)
# 1      2 
# 3      1
for k in np.arange(9)+1:
  print(">> k = "+str(k));   print( CpM[Cgroup==k] )
# >> k = 1 ---> 購買 kind16/kind2 的客群
# cat7      kind1  kind11  kind12  kind16  kind17  kind2  kind3  others
# customer                                                             
# c372         26      14       0     127       8     43     11      22
# c391         11       5       1      76       6     60      6      11
# >> k = 2 ---> 購買 kind2 的客群 (25人)
# cat7      kind1  kind11  kind12  kind16  kind17  kind2  kind3  others
# customer                                                             
# c111          0       4       0       5       0     55     16       3
# c1155         0       0       3       0       0     47      9       1
# c120          0       3       1       7       1     93      4       4
# c126          0       1       8       0       0     94      0       3
# ...

#%%##===== (2F4) 消費基因: 各類別的特徵 (CpM+Cgroup-->Gfeature) =====#####
for k in np.arange(9)+1:
    A = CpM[Cgroup==k].mean();  # print(A)
    B = 100*A/sum(A);           # print(B)
    ABk = pd.DataFrame({"mean-"+str(k):list(A), "prop-"+str(k):list(B)});   print(ABk)
    if (k==1):
        AB = ABk
    else:
        AB = pd.concat([AB, ABk], axis=1);  print(AB)
Gfeature = AB.T.round(2);   Gfeature.columns = list(CpM.columns);   print(Gfeature)
#         kind1  kind11  kind12  kind16  kind17   kind2  kind3  others   人數
# mean-1  18.50    9.50    0.50  101.50    7.00   51.50   8.50   16.50 --  2 ---> 多購買(kind16/kind2/others/kind1)
# prop-1   8.67    4.45    0.23   47.54    3.28   24.12   3.98    7.73

# mean-2   3.44    2.40    8.52    2.88    4.20   60.60   7.64    3.84 -- 25 =====> 多kind2
# prop-2   3.68    2.57    9.11    3.08    4.49   64.80   8.17    4.11

# mean-3  36.00   53.00    0.00    0.00   37.00  144.00   7.00    2.00 --  1 ---> 大量購買(kind2/kind11/kind17/kind1)
# prop-3  12.90   19.00    0.00    0.00   13.26   51.61   2.51    0.72

# mean-4  76.00    2.83    8.58    0.08    2.42    9.67   4.33   16.25 -- 12 =====> 大量kind1 + others
# prop-4  63.25    2.36    7.14    0.07    2.01    8.04   3.61   13.52

# mean-5  22.30    1.27    2.70    1.08    0.54    6.98   1.71    4.70 -- 97 =====> 多kind1 + kind2
# prop-5  54.02    3.07    6.54    2.62    1.30   16.91   4.15   11.39

# mean-6   0.00    0.80    0.00    0.00    0.00    3.80   0.40   64.80 --  5 ---> 購買其他類(others)
# prop-6   0.00    1.15    0.00    0.00    0.00    5.44   0.57   92.84

# mean-7   4.20    1.13    5.00    0.40   33.40    6.93   1.00    1.40 -- 15 =====> kind17
# prop-7   7.86    2.12    9.35    0.75   62.47   12.97   1.87    2.62

# mean-8   2.12    1.58    5.27    3.22    0.64   24.60   3.36    2.87 -- 77 =====> kind2
# prop-8   4.85    3.63   12.08    7.38    1.46   56.34   7.70    6.57

# mean-9   2.10    1.29    3.41    1.89    0.32    9.68   5.70    3.77 --133 ---> 一般群: 沒有明顯特
# prop-9   7.45    4.57   12.10    6.71    1.12   34.41  20.25   13.38

##== 客戶消費基因(customer consumption gene): 以購買品類描述客戶的消費特徵
##== 消費族群(consumption species): 具有相同消費基因的客戶族群
##== 消費演化(consumption evolution): 客戶從一個世代(generation, 時間段)到下一個世代的消費行為演化

#%%##===== [實作2-5] 這裡的消費基因，要怎樣加作前面的互動網站呢? =====#####

#%%####### (2G) 人工智能(AI)的決策 (1.5hr) ##########

#%%##===== (2G1) AI (Artificial Intelligence) 的範疇 =====#####

##== (1).符號式AI (Symbolic AI) ==###
#   -- 與邏輯(logic)相關
#   -- 通常表示成生產規則(production rule): IF 條件 THEN 結論
#   -- 有 version space, 演繹學習(deductive learning)，歸納學習(inductive learning)等各種方法
#   -- 形成專家系統 (expert system): 通常分成 規則庫、工作記憶、推理引擎
#   -- 問題：很難習得知識(規則) -- 知識擷取(knowledge acquisition) --> 機器學習(machine learning) 
##== (2).數值式AI (Numeric AI) ==###
#== 神經網絡 (neural network) -- 連結主義 (connectionism)
#   -- 模仿生物單一個體的學習
#   -- 2014年開始，進入深度學習(deep learning)
#== 基因演算法(genetic algorithm) -- 演化理論 (evolution theory)
#   -- 模仿生物群體的學習
#   -- 有螞蟻演算法，文化模型，免疫模型等變化型
##== (3) 監督式模型的設計 (x-->y) =====#####
#-- M: x = ["channel","CvMM0"] ---> y = "cat7"
x = XXXFM[["cat7","CvMM0"]];   print(x.shape);   print(x.head(2))   #-- (16746, 2)
#     cat7            CvMM0
# 7  kind1  (99999, 999999]
# 8  kind1  (99999, 999999]
y = XXXFM[["channel"]];   print(y.shape)       #-- (16746, 1)

#%%##===== (2G2) 數據的編碼 (x-->xx) =====#####

#%%== (1).Label Encoding: 把每個類別 mapping 到某個整數，不會增加新欄位
from sklearn.preprocessing import LabelEncoder 
labelencoder = LabelEncoder()
xx = x.copy();   
xx['cat7']  = labelencoder.fit_transform(xx['cat7'])
xx['CvMM0'] = labelencoder.fit_transform(xx['CvMM0'])
print(xx.shape);   print(xx.iloc[10000:10002])
#        cat7  CvMM0
# 35611     5      0
# 35615     5      1

#%%== (2).One Hot Encoding: 為每個類別新增一個欄位，用 0/1 表示是否
from sklearn.preprocessing import OneHotEncoder
onehotencoder = OneHotEncoder(categories='auto')
xx = onehotencoder.fit_transform(x).toarray()
print(xx.shape);   print(xx[10000:10002])   #-- (16746, 10)
# [[0. 0. 0. 0. 0. 1. 0. 0. 1. 0.]
#  [0. 0. 0. 0. 0. 1. 0. 0. 0. 1.]]

#%%== (3).pandas中的 one-hot encoding: 除了編碼外, 還具有欄位名稱 
xx = pd.get_dummies(x);   print(xx.shape);   print(xx.iloc[0])   #-- (16746, 10)
# cat7_kind1               1
# cat7_kind11              0
# cat7_kind12              0
# cat7_kind16              0
# cat7_kind17              0
# cat7_kind2               0
# cat7_kind3               0
# cat7_others              0
# CvMM0_(9999, 99999]      0
# CvMM0_(99999, 999999]    1
       
#%%##===== (2G3) 數據規畫 (Data Planning) =====#####

##== (1).數據分割 (Data Partition): 數據集分成 --
#        (A).訓練數據組 (training data, seen data): 用以建立模式及其參數 
#        (B).測試數據組 (testing data, unseen data): 用以評估訓練數據, 所建立的模式, 是否過度複進或其通用性
#        (C).驗證數據組(validation/tuning data): 用以衡量模式的好壞, 並調整模型

##== (2).常用的數據分割的方法:
#        (A).留出法(hold-out): 抽取80%的數據用以建構模式, 剩下的20%用於模式的效度檢驗 train_test_split
#        (B).k-fold交互驗證(k-fold cross-validation): KFold, GroupKFild, StratifiedKFold 
#            -- 將數據分為 k 個等分，每次選取 k-1 份進行模式訓練，剩下的一份數據則用以測試模式。
#            -- 如此重複 k 次，使每筆數據都能成為訓練數據集與測試數據集，最後的平均結果代表模式的效度。
#        (C).leave-one-out cross-validation: 當k個區間等於總樣本數時: LeaveOneGroupOut，LeavePGroupsOut，LeaveOneOut，LeavePOut
#        (D).自助法(bootstraping): 使用重複取樣的方式進行數據取樣: 自定函式

##== (3).留出法函式: 數據直接取樣函式(X/y_train)及測試數據(X/y_test) -- 隨機抽樣
#        (A).將數據集 X 劃分為 訓練集X_train 及 測試集 X_test
#        (B).通常以 2/3~4/5 的數據用於訓練，test_size 預設值為 0.25
#        (C).亦可設定 test_size 為測試數量，另亦可設定訓練數據 train_size
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(xx , y, test_size=0.2)
print(X_train.shape);   print(X_test.shape)   #-- (13396, 10)   (3350, 10)
print(y_train.shape);   print(y_test.shape)   #-- (13396, 1)   (3350, 1)

#%%##===== (2G4) (KDD4) 決策樹 (Decision Tree) =====#####
from sklearn.tree import DecisionTreeClassifier
model = DecisionTreeClassifier()
clf = model.fit(X_train, y_train)  ##== (2E1-A) 訓練階段(Learning/Modeling/Estimation/Training Phase): (u, y) -> M#
y_predict = clf.predict(X_test)    ##== (2E1-B) 預測階段(Prediction/Production/Application Phase): (u_new, M#) -> y_predict
print(len(y_predict));   print(y_predict[0:10])   #-- 3350  ['s3' 's3' 's3' 's2' 's2' 's2' 's2' 's2' 's2' 's2']

#%%##===== (2G5) (KDD5) 決策樹中的規則/知識 =====#####
##== (1).決策樹分為 決策節點 與 終端節點
#        (A).決策節點: 是一個屬性的條件式, 如: cat7_kind11 >  0.50 (表示: cat7_kind11 = 1, 即 cat7_kind11)
#        (B).終端節點: 表示一條規則, 如: 
#            (R17B) IF (cat7_kind1<=0.5) AND (cat7_kind17>0.5) AND ( CvMM0_(9999, 99999]>0.50) THEN s5
##== (2).決策樹之列表顯示:
from sklearn.tree import export_text
print( export_text(clf, feature_names=list(xx.columns)) )  #--> "(9999, 99999]": 萬元客, "(99999, 999999]": 十萬元客 
# |--- cat7_kind1 <= 0.50
# |   |--- cat7_kind17 <= 0.50
# |   |   |--- cat7_others <= 0.50
# |   |   |   |--- cat7_kind16 <= 0.50
# |   |   |   |   |--- cat7_kind3 <= 0.50
# |   |   |   |   |   |--- cat7_kind2 <= 0.50
# |   |   |   |   |   |   |--- cat7_kind11 <= 0.50
# |   |   |   |   |   |   |   |--- CvMM0_(9999, 99999] <= 0.50 ===> IF (CvMM0="(99999, 999999]") THEN s3
# |   |   |   |   |   |   |   |   |--- class: s3
# |   |   |   |   |   |   |   |--- CvMM0_(9999, 99999] >  0.50 ===> IF (CvMM0="(9999, 99999]") THEN s2
# |   |   |   |   |   |   |   |   |--- class: s2
# |   |   |   |   |   |   |--- cat7_kind11 >  0.50
# |   |   |   |   |   |   |   |--- CvMM0_(99999, 999999] <= 0.50 ===> IF (CvMM0="(99999, 999999]") AND (kind11) THEN s2
# |   |   |   |   |   |   |   |   |--- class: s2                        萬元客 會在 s2 買 kind11
# |   |   |   |   |   |   |   |--- CvMM0_(99999, 999999] >  0.50 ===> 十萬元客 會在 s2 買 kind11
# |   |   |   |   |   |   |   |   |--- class: s2
# |   |   |   |   |   |--- cat7_kind2 >  0.50
# |   |   |   |   |   |   |--- CvMM0_(9999, 99999] <= 0.50  ===> 十萬元客 會在 s2 買 kind2
# |   |   |   |   |   |   |   |--- class: s2
# |   |   |   |   |   |   |--- CvMM0_(9999, 99999] >  0.50  ===>   萬元客 會在 s2 買 kind2
# |   |   |   |   |   |   |   |--- class: s2
# |   |   |   |   |--- cat7_kind3 >  0.50
# |   |   |   |   |   |--- CvMM0_(99999, 999999] <= 0.50  ===>   萬元客 會在 s2 買 kind3
# |   |   |   |   |   |   |--- class: s2
# |   |   |   |   |   |--- CvMM0_(99999, 999999] >  0.50  ===> 十萬元客 會在 s2 買 kind3
# |   |   |   |   |   |   |--- class: s2
# |   |   |   |--- cat7_kind16 >  0.50
# |   |   |   |   |--- CvMM0_(9999, 99999] <= 0.50  ===> 十萬元客 會在 s4 買 kind16
# |   |   |   |   |   |--- class: s4
# |   |   |   |   |--- CvMM0_(9999, 99999] >  0.50  ===>   萬元客 會在 s2 買 kind16
# |   |   |   |   |   |--- class: s2
# |   |   |--- cat7_others >  0.50
# |   |   |   |--- CvMM0_(99999, 999999] <= 0.50  ===>   萬元客 會在 s2 買 others
# |   |   |   |   |--- class: s2
# |   |   |   |--- CvMM0_(99999, 999999] >  0.50  ===> 十萬元客 會在 s3 買 others
# |   |   |   |   |--- class: s3
# |   |--- cat7_kind17 >  0.50
# |   |   |--- CvMM0_(9999, 99999] <= 0.50  ===> 十萬元客 會在 s5 買 kind17 (R17A)
# |   |   |   |--- class: s5
# |   |   |--- CvMM0_(9999, 99999] >  0.50  ===>   萬元客 會在 s5 買 kind17 (R17B)
# |   |   |   |--- class: s5
# |--- cat7_kind1 >  0.50
# |   |--- CvMM0_(99999, 999999] <= 0.50  ===>   萬元客 會在 s3 買 kind1
# |   |   |--- class: s3
# |   |--- CvMM0_(99999, 999999] >  0.50  ===> 十萬元客 會在 s3 買 kind1
# |   |   |--- class: s3
##== (3).決策樹之圖形顯示:
from sklearn.tree import plot_tree
plot_tree(clf, feature_names=list(xx.columns) )   #-- 此函式繪圖不甚清楚, 還有其他方式, 在此暫略

#%%##===== (2G6) (KDD5數據解讀/評估) (決策樹)分類決策模型之評估 =====#####

##== (1A).雙分類混淆矩陣 (Two-class confusion matrix) ==###
#                                    ACTUAL CLASS
#                               positive          negative
# PREDICTED    positive   True Positives   False Positives <-- type-I error (alpha)
# CLASS                             (TP)              (FP)
#              negative  False Negatives    True Negatives
#                                   (FN)              (TN)
#               type-II error (beta) --^
#                 power of test = 1-beta

##== (1B).多分類混淆矩陣 ==###
from sklearn.metrics import confusion_matrix
print(confusion_matrix(y_test, y_predict))
# [[   0  301  260    0    0]
#  [   0 1244   15   13    7]
#  [   0   99  527    0    3]
#  [   0  348   56   20    9]
#  [   0  293    9    0  146]]

#%%== (2) 精確度(precision): P = TP / (TP+FP)
from sklearn import metrics
print("(1) 精確度(precision): P = TP / (TP+FP) ")
print(metrics.precision_score(y_test, y_predict, average='micro'))   #-- 精確度 P = 0.5782089552238806
##== (3) 召回率(recall) R = TP / (TP+FN)
print("(2) 召回率(recall) = TP / (TP+FN) ")
print(metrics.recall_score(y_test, y_predict, average='micro'))      #-- 召回率 R = 0.5782089552238806
##== (4) F1 = 2*P*R/(P+R) --> P 和 R 的調和平均數
print("(3) F1-value: F1 = 2*P*R/(P+R) ") 
print(metrics.f1_score(y_test, y_predict, average='micro'))          #-- F1-value F1 = 0.5782089552238806

#%%##===== [實作2-6] 您的網站系統中，有機會加進這種決策規則嗎? =====#####

