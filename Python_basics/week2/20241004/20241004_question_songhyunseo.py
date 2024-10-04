# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import plotly
import yfinance as yf
import plotly.graph_objects as go

# 서술형 문제 1
"""
1. 
git 에서 레포지토리 이름 alphaco 생성, 이때 git ignore는 python,  readMe는 생성에 체크하여 레포지토리를 생성한다. 
이후 레포지토리 코드 링크를 복사한 다음, 원하는 위치에 git bash를 연 다음 'git clone 레포지토리 링크' 로 로컬에
레포지토리를 생성한다.

파일 main.py를 실행시키기 전, 먼저 라이브러리 버전 퉁돌 방지와 독립성 유지를 위해 가상 환경을 설정해주어야 한다.
방법은 conda와 virtualenv가 있으나, virtualenv가 더 쉽기 때문에 그 방법을 사용한다.
virtualenv venv로 가상 환경을 킨 후, source venv/Scripts/activate로 가상 환경을 활성화시켜 줘야 한다.
이후 which python을 통해 현재 작동중인 파이썬이 venv아래 있다면 가상 환경이 성공적으로 설정된 것이다.

파일 main.py를 만든 후 git에 연동하려면, 먼저 협업 중이라면 레포지토리에 변경 사항이 있을 수 있으므로 해당 변경 사항을 
로컬에 적용시키기 위해 git pull을 한다. 아니라면, git add . 로 현재 로컬 레포지토리의 변경 사항을 commit할 리스트에 전부
추가시킨다. 이때 . 는 전체를 의미하므로 원하는 일부만 add 하고 싶다면 . 이 아니라 특정 파일/폴더를 지정해 줄 수 있다.
이후 git commit -m "update_message" 를 사용하여 임의의 업데이트 메시지와 함께 커밋을 진행한다. 여기까지 끝냈다면 마지막으로
git push를 통해 깃허브에 내 커밋 사항을 연동시키면 된다.
"""

# 코드 문제 1
result = []
for i in range(10):
    if i % 2 == 0:
        result.append(i * 2)
print(result)

# 답지
code_result1 = [i*2 if i % 2 == 0 else i for i in range(10)]
print(code_result1)

# 코드 문제 2
my_dict = {'apple': 3, 'banana': 5, 'orange': 2}

# 답지
for key, value in my_dict.items():
    print(f'{key}: {value}')


# 코드 문제 3
series = pd.Series([25, 35, 45, 60, 75])

# 답지
# np.where를 사용하여 조건 적용
code_result3 = np.where((series > 30) & (series < 60), series + 10 , series)

# 결과 출력
print(code_result3)

# 코드 문제 4
iris = sns.load_dataset("iris")

# 답지
iris.to_csv("output/code4_songhyunseo.csv", index = False)
iris.to_excel("output/code4_songhyunseo.xlsx", index = False)




# 코드 문제 5
data = [
    ["1,000", "1,100", '1,510'],
    ["1,410", "1,420", '1,790'],
    ["850", "900", '1,185'],
]
columns = ["03/02", "03/03", "03/04"]
df = pd.DataFrame(data=data, columns=columns)
#df.info()

# 답지

def rm_comma(df):
    df_fixed = df.apply(lambda x: x.replace(',', "")).astype(int)
    return df_fixed

df['03/02'] = rm_comma(df['03/02'])
df['03/03'] = rm_comma(df['03/03'])
df.info()


# 코드 문제 6
"""
apple = yf.download("AAPL", start="2020-01-01", end = "2024-09-30")
fig, ax = plt.subplots()
ax.plot(apple['Open'], label = "Apple")
ax.legend()
plt.show()
"""
# 답지
apple = yf.download("AAPL", start="2020-01-01", end = "2024-09-30")
fig, ax = plt.subplots()
ax.plot(apple['Open'], label = "Apple")
ax.legend()
plt.show()

plt.savefig("output/code6_songhyunseo.png")

# 코드 문제 7
tips = sns.load_dataset("tips")

# 답지
fig, ax = plt.subplots()
ax.scatter(tips)

plt.savefig("output/code7_songhyunseo.png")
"""
# 코드 문제 8
apple = yf.download("AAPL", start="2024-05-01", end="2024-09-30")

# 답지
# 여기서부터 코드 작성
"""