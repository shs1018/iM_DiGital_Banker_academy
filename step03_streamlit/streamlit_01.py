import time
import numpy as np
import pandas as pd
import streamlit as st
import streamlit.components.v1 as components

st.write("Hello World!")
st.write("Hello World!!")

st.title("This is a title")
st.title("_Streamlit_ is :blue[cool] :sunglasses:")

_LOREM_IPSUM = """
Lorem ipsum dolor sit amet, **consectetur adipiscing** elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
"""

def stream_data():
    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)

    yield pd.DataFrame(
        np.random.randn(5, 10),
        columns=["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"],
    )

    for word in _LOREM_IPSUM.split(" "):
        yield word + " "
        time.sleep(0.02)


if st.button("Stream data"):
    st.write_stream(stream_data)


st.markdown("HTML CSS 마크다운 적용")
html_css = """
<style>
    table.customTable {
    width: 100%;
    background-color: #FFFFFF;
    border-collapse: collapse;
    border-width: 2px;
    border-color: #7ea8f8;
    border-style: solid;
    color: #000000;
    }
</style>

<table class="customTable">
    <thead>
    <tr>
        <th>이름</th>
        <th>나이</th>
        <th>직업</th>
    </tr>
    </thead>
    <tbody>
    <tr>
        <td>Evan</td>
        <td>25</td>
        <td>데이터 분석가</td>
    </tr>
    <tr>
        <td>Sara</td>
        <td>25</td>
        <td>프로덕트 오너</td>
    </tr>
    </tbody>
</table>
"""

st.markdown(html_css, unsafe_allow_html=True)

st.markdown("HTML JS Streamlit 적용")
js_code = """ 
<h3>Hi</h3>

<script>
function sayHello() {
    alert('Hello from JavaScript in Streamlit Web');
}
</script>

<button onclick="sayHello()">Click me</button>
"""
components.html(js_code)