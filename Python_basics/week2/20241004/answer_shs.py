from pandas import DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

'''
문제 1
개발환경설정 및 깃허브 push 전과정 서술
'''

'''
그 외 문제는 실습 시 진행했던 코드에서 거의 판박이 수준. 
colname이나 범위가 살짝 바뀌는 정도로 예상된다.
판다스 슬라이싱/ 시각화

오늘 - 내일 복습하다가 안되는 거 있으면 즉시 질문하기

문제지는 프린트로 제공된다.

output <- 시각화 이미지/ 전처리된 csv 저장하는 위치.
이미지/ csv 저장하는 방법 복습하기.
'''

# data = pd.read_csv('C:/Users/1018g/OneDrive/바탕 화면/playground-series-s4e9/sample_submission.csv')

from pandas import DataFrame
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

data = [
    ["2차전지(생산)", "SK이노베이션", 10.19, 1.29],
    ["해운", "팬오션", 21.23, 0.95],
    ["시스템반도체", "티엘아이", 35.97, 1.12],
    ["해운", "HMM", 21.52, 3.20],
    ["시스템반도체", "아이에이", 37.32, 3.55],
    ["2차전지(생산)", "LG화학", 83.06, 3.75]
]

columns = ["테마", "종목명", "PER", "PBR"]
df = DataFrame(data=data, columns=columns)

#--

df = pd.read_excel('C:/Users/1018g/OneDrive/바탕 화면/iM DBA/ss_ex_1.xlsx', parse_dates = ['일자'])
#df['일자'] = pd.to_datetime(df['일자'])

def set_time_cols(data):
  data['분기'] = data['일자'].dt.quarter
  data['연도'] = data['일자'].dt.year
  data['월'] = data['일자'].dt.month
  data['일'] = data['일자'].dt.day
  data = data.drop(columns = ['일자'])
  return data

df2 = set_time_cols(df)
#print(df2.info())


the_great_filter = {
  '시가': 'first',
  '종가': 'last',
  '고가': 'max',
  '저가': 'min',
  '거래량': "sum"
}

#print(df2.groupby(['연도', '분기']).agg(the_great_filter))