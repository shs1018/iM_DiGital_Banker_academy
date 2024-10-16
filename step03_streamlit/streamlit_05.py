# -*- coding: utf-8 -*-
import streamlit as st 
import pandas as pd 
import numpy as np 
import matplotlib.pyplot as plt

def cal_sales_revenue(price, total_sales):
    revenue = price * total_sales
    return revenue

def main():
    st.title("여기에서부터 시작")
    price = st.slider("단가:", 1, 1000, value=500)
    total_sales = st.slider("판매갯수:", 1, 1000, value=500)
    print(price, total_sales)
    st.write("단가:", price, "판매갯수:", total_sales)

    if st.button("매출액 계산"):
        revenue = cal_sales_revenue(price, total_sales)
        st.write(revenue)

    st.title('Check Box Control')
    x = np.linspace(0, price, total_sales)
    y = np.sin(x)
    z = np.cos(x)
    show_plot = st.checkbox("시각화 보여주기")
    print(show_plot) 
    if show_plot:
        fig, ax = plt.subplots()
        ax.plot(x, y)
        ax.plot(x, z)
        st.pyplot(fig)
 
if __name__ == "__main__":
    main()
