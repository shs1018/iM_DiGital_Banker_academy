# -*- coding: utf-8 -*-
import streamlit as st 
import pandas as pd 


# 캐시메모리는 대용량 데이터는 불러오면 안됨
# 현업 : SQL 데이터 가공을 일부 진행
# 쉽게 말하면 Raw 데이터는 끌고 오면 안됨
@st.cache_data
def load_data():
    train = pd.read_csv('./data/train.csv')
    return train 

def main():
    st.title("여기에서부터 시작")

    train = load_data()
    print(train.head())
    st.dataframe(train, width=100)
    st.data_editor(train)
    # st.table(train) 가급적 쓰지 말자

    data_df = pd.DataFrame(
        {
            "sales": [
                [0, 4, 26, 80, 100, 40],
                [80, 20, 80, 35, 40, 100],
                [10, 20, 80, 80, 70, 0],
                [10, 100, 20, 100, 30, 100],
            ],
        }
    )
    st.dataframe(data_df)

    st.data_editor(
        data_df,
        column_config={
            "sales": st.column_config.BarChartColumn(
                "Sales (last 6 months)",
                help="The sales volume in the last 6 months",
                y_min=0,
                y_max=100,
            ),
        },
        hide_index=True,
    )

if __name__ == "__main__":
    main()
