
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.formula.api import ols
from statsmodels.stats.anova import anova_lm

ori = pd.read_csv('./datasets/Adidas_US_Sales_Datasets.csv')

# 데이터 전처리
df = ori.copy()
df['Retailer ID'] = df['Retailer ID'].astype('str')
df['Price per Unit'] = df['Price per Unit'].str.replace('[$%,]', '', regex=True).astype('float')
df['Units Sold'] = df['Units Sold'].str.replace('[$%,]', '', regex=True).astype('float')
df['Total Sales'] = df['Total Sales'].str.replace('[$%,]', '', regex=True).astype('float')
df['Operating Profit'] = df['Operating Profit'].str.replace('[$%,]', '', regex=True).astype('float')
df['Operating Margin'] = df['Operating Margin'].str.replace('[$%,]', '', regex=True).astype('float')
df['Operating Margin'] = df['Operating Margin'] * 0.01
df['Invoice Date'] = pd.to_datetime(df['Invoice Date'])
df['year'] = df['Invoice Date'].dt.year
df['month'] = df['Invoice Date'].dt.month

# 이미지 및 테이블 생성 함수
def sales_plot():
    fig = plt.figure(figsize=(8, 6))
    df.groupby(['year', 'month'])['Units Sold'].sum().plot()
    plt.ylabel('Sum of Units Sold')
    st.pyplot(fig)

def retail_plot():
    fig, ax = plt.subplots(figsize=(20, 8))
    df.pivot_table(index=['year', 'month'], columns='Retailer', values='Units Sold', aggfunc='sum').plot(ax=ax)
    st.pyplot(fig)

def brand_retail_count_plot():
    df2 = df[['Retailer', 'Retailer ID', 'year', 'month']].drop_duplicates().sort_values(['Retailer', 'year', 'month'])
    fig, ax = plt.subplots(figsize=(20, 8))
    df2.pivot_table(index=['year', 'month'], columns='Retailer', values='Retailer ID', aggfunc='count').plot(kind='area', ax=ax)
    st.pyplot(fig)

def method_sales_plot(val='Units Sold'):
    fig, ax = plt.subplots(figsize=(20, 10))
    df.pivot_table(index=['year', 'month'], columns='Sales Method', values=val, aggfunc='mean').plot(ax=ax)
    st.pyplot(fig)

def method_sales_boxplot():
    fig, ax = plt.subplots()
    df[['Sales Method', 'Price per Unit']].boxplot(by='Sales Method', ax=ax)
    plt.grid(False)
    st.pyplot(fig)

def method_margin_boxplot():
    fig, ax = plt.subplots()
    sns.boxplot(data=df, x='Sales Method', y='Operating Margin', ax=ax)
    st.pyplot(fig)

def anova_analysis(x, y):
    df_anova = df[[x, y]]
    if ' ' in x:
        x = x.replace(' ', '_')
    if ' ' in y:
        y = y.replace(' ', '_')
    df_anova.columns = [x, y]
    model = ols(f'{y} ~ C({x})', data=df_anova).fit()
    anova_tbl = anova_lm(model)
    return anova_tbl


st.sidebar.title("Adidas US Sales Analysis")
# option = st.sidebar.selectbox("Choose a section", ["연-월별 데이터 분석", "판매 방법에 따른 데이터분석", "판매 방법에 따른 마진율 분산분석"])
pages = ["연-월별 데이터 분석", "판매 방법에 따른 데이터분석", "판매 방법에 따른 마진율 분산분석"]
option = st.sidebar.radio("Go to", pages)

if option == "연-월별 데이터 분석":
    tabs = st.tabs(["Sales", "Retail", "Brand Retail Count"])
    
    with tabs[0]:
        st.header("Sales Plot")
        sales_plot()
        st.write("연-월별 판매량을 보여주는 그래프입니다. 특정 시점에서 판매량의 급증을 확인할 수 있습니다.")

    with tabs[1]:
        st.header("Retail Plot")
        retail_plot()
        st.write("연-월별 소매업체별 판매량을 보여주는 그래프입니다. 특정 소매업체에서 판매가 시작된 시점을 확인할 수 있습니다.")
        
    with tabs[2]:
        st.header("Brand Retail Count")
        brand_retail_count_plot()
        st.write("연-월별 브랜드별 소매점 수를 보여주는 그래프입니다. 특정 시점에서 소매점 수의 증가를 확인할 수 있습니다.")
        
elif option == "판매 방법에 따른 데이터분석":
    tabs = st.tabs(["Sales Plot", "Box Plot"])
    
    with tabs[0]:
        st.header("Sales Plot")
        val = st.selectbox("Select a metric", ['Units Sold', 'Price per Unit', 'Total Sales'])
        method_sales_plot(val)
        
    with tabs[1]:
        st.header("Box Plot")
        radio_val = st.radio("Select a distribution", ['단가 분포', '영업이익 분포'])
        if radio_val == '단가 분포':
            method_sales_boxplot()
        else:
            method_margin_boxplot()

elif option == "판매 방법에 따른 마진율 분산분석":
    st.header("판매 방법에 따른 마진율 분산분석")
    y = st.selectbox("Select a variable", ['Operating Margin', 'Price per Unit'])
    result = anova_analysis('Sales Method', y)
    st.write(result)
    st.write("ANOVA 결과를 통해 판매 방법에 따른 선택 변수의 유의미한 차이를 확인할 수 있습니다.")
