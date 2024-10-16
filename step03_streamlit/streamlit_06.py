import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# 데이터 불러오기
@st.cache_data
def load_data():
    df = sns.load_dataset('iris')
    return df

def plot_matplotlib(df):
    st.title('Scatter Plot with Matplotlib')
    fig, ax = plt.subplots()
    ax.scatter(df['sepal_length'], df['sepal_width'])
    st.pyplot(fig)

def plot_seaborn(df):
    st.title('Scatter Plot with Seaborn')
    fig, ax = plt.subplots()
    sns.scatterplot(df, x = 'sepal_length', y = 'sepal_width')
    st.pyplot(fig)

def plot_plotly(df):
    st.title('Scatter Plot with Plotly')
    fig = go.Figure()
    fig.add_trace(
        go.Scatter(x = df['sepal_length'],
                   y = df['sepal_width'],
                   mode='markers')
    )
    st.plotly_chart(fig)

def main():
    st.title("Choose a plotting library")
    iris = load_data()
    st.data_editor(iris)

    plot_type = st.radio(
        "어떤 스타일의 산점도를 보고 싶은가요?",
        ("Matplotlib", "Seaborn", "Plotly"))
    
    st.write(plot_type)

    if plot_type == "Matplotlib":
        plot_matplotlib(iris)
    elif plot_type == "Seaborn":
        plot_seaborn(iris)
    elif plot_type == "Plotly":
        plot_plotly(iris)

if __name__ == '__main__':
    main()