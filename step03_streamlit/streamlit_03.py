# -*- coding: utf-8 -*-
import pandas as pd 
import seaborn as sns
import streamlit as st
import matplotlib.pyplot as plt

@st.cache_data
def load_data():
    df = pd.read_csv('./data/train.csv')
    return df

def main():
    pass

if __name__ == "__main__":
    main()