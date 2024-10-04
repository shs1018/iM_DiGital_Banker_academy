from pandas import *
import os

#먼저 저장할 데이터를 만들자...
data = {
    "종목명": ["3R", "3SOFT", "ACTS"],
    "현재가": [1510, 1790, 1185],
    "등락률": [7.36, 1.65, 1.28],
}

data = DataFrame(data)

if not os.path.isdir('abc'):    #현재 디렉토리에 abc가 없다면...
    os.mkdir("abc")             #현재 디텍토리에 abc폴더를 만들어라!!

data.to_csv("abc/data.csv", index = False)
data.to_excel("abc/data.xlsx", index = False)