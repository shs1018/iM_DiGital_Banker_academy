# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd

'''
캐시메모리는 대용량 데이터를 불러오면 안됨
현업 : SQL데이터 가공을 일부 진행
쉽게 말하면 Raw 데이터(1GB이상)은 끌고 오면 안됨
'''
@st.cache_data 
def load_data():
    train = pd.read_csv('/data/train.csv')
    return train




def main():
    st.title("Let's get started!")

    train = load_data()
    print(train.head)
    # 데이터가공
    m_tips = tips.loc[tips['sex'] == 'Male', :]
    f_tips = tips.loc[tips['sex'] == 'Female', :]

    # 시각화 차트
    fig, ax = plt.subplots(ncols=2, figsize=(10, 6), sharex=True, sharey=True)
    ax[0].scatter(x = m_tips['total_bill'], y = m_tips['tip'])
    ax[0].set_title('Male')
    ax[1].scatter(x = f_tips['total_bill'], y = f_tips['tip'])
    ax[1].set_title('Female')

    # 중요포인트
    # plt.show()
    st.pyplot(fig)n



if __name__ == "__main__":
    main()