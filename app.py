
import streamlit as st

year = st.slider('연도를 선택하세요', 2000, 2020)
hobby = st.selectbox('다음 중 취미를 선택하세요', ('읽기', '여행', '요리'))
st.write(f'당신은 연도는 {year}와 취미는 {hobby}를 선택하셨습니다.')
