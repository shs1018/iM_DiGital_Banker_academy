import streamlit as st
import streamlit.components.v1 as components

st.write('Hello Streamlit!')
st.write('Good bye Streamlit!')

def main():
    st.title("This is Text Elements")
    st.header("This is Header/헤더")
    st.subheader("This is sub Header")
    st.write("파이썬 문법 사용 가능")
    st.write("-" * 50) # print()
    st.markdown(""" 
    ## Chapter 1. 
    - 색상 테스트 : This text is :red[colored red], and **:blue[colored]** and bold.
    """)
    st.markdown(""" 
    ### SubChapter 1. 
    - 피타고라스 정리 : :red[$\sqrt{x^2+y^2}=1$] is a Pythagorean identity. :pencil:
    """)
    st.markdown("## Chapter 2. \n"
                "- Streamlit is **_really_ cool**.\n"
                "   * This text is :blue[colored blue], and this is **:red[colored] ** and bold.")
    

if __name__ == "__main__":
    main()

def main():
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



if __name__ == "__main__":
    main()

