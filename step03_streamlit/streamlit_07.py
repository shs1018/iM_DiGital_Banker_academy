# -*- coding: utf-8 -*-
import streamlit as st
import pandas as pd
import seaborn as sns

# 데이터 불러오기
@st.cache_data
def load_data():
    df = sns.load_dataset('iris')
    return df

def main():
    st.title("SelectBox 사용")
    iris = load_data()
    st.markdown("## Raw Data")
    st.dataframe(iris)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("## Select")
    val = st.selectbox("1개의 종을 선택하세요", iris.species.unique())
    st.write("선택된 species : ", val)
    iris2 = iris.loc[iris['species'] == val, :].reset_index(drop=True)
    st.dataframe(iris2)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("## MultiSelect")
    cols = st.multiselect("복수의 컬럼을 선택하세요", iris.columns)
    st.write("선택된 컬럼 : ", cols)
    st.dataframe(iris.loc[:, cols])
    

if __name__ == '__main__':
    main()
