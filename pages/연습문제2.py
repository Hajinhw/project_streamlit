# 1. iris 데이터셋을 이용하여
import streamlit as st
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
from konlpy.tag import Okt
from collections import Counter
import json
import folium
from streamlit_folium import st_folium

# 1) iris 데이터셋을 데이터프레임으로 표시
iris = sns.load_dataset('iris')
st.subheader('iris 데이터프레임')
st.write(iris)
st.divider()

# 2) multiselect를 사용하여 품종을 선택하면, 해당 품종에 대한 데이터를 데이터프레임으로 표시
st.subheader('각 품종에 대한 정보')
sp = st.multiselect('품종을 선택해 주세요',
               ['setosa', 'versicolor', 'virginica'], default='setosa')

if len(sp) == 1:
    st.dataframe(iris[iris['species'] == sp[0]])
elif len(sp) == 2:
    col1, col2 = st.columns(2)
    col1.dataframe(iris[iris['species'] == sp[0]])
    col2.dataframe(iris[iris['species'] == sp[1]])
else:
    col1, col2, col3 = st.columns(3)
    col1.dataframe(iris[iris['species'] == sp[0]])
    col2.dataframe(iris[iris['species'] == sp[1]])
    col3.dataframe(iris[iris['species'] == sp[2]])

st.divider()

# 3) 품종을 제외한 4가지 컬럼을 radio 요소를 사용하여 선택하면
#   선택한 컬럼에 대한 히스토그램 그리기(matplotlib)
st.subheader('히스토그램')
columns = st.radio(
    label = '어떤 정보를 알고 싶으신가요?',
    options = ['sepal_length', 'sepal_width', 'petal_length', 'petal_width'],
    captions=['꽃받침 길이', '꽃받침 너비', '꽃잎 길이', '꽃잎 너비'],
    horizontal=True)

def col_to_hist(col):
    if columns == col:
        fig, ax = plt.subplots()
        ax.hist(iris[col])
        st.pyplot(fig)

col_to_hist('sepal_length')
col_to_hist('sepal_width')
col_to_hist('petal_length')
col_to_hist('petal_width')
st.divider()

# 2. kor_news 데이터셋을 이용
# 분류의 대분류 기준을 선택하면 해당 분야의 주요 키워드 20위에 대한 bar chart 표시
df = pd.read_excel('data/kor_news_240326.xlsx')
st.subheader('뉴스 대분류 주요 키워드 Top20')
df['대분류'] = df.분류.str.split('>').str[0]
okt = Okt()
def title_to_tokens(df, sub):
    df_eco = df[df['대분류']==sub]
    df_title = list(df_eco['제목'].values)
    tokens_df = [okt.nouns(title) for title in df_title]
    tokens_title = sum(tokens_df, [])
    tokens_title2 = [token for token in tokens_title if len(token) > 1]
    return tokens_title2

def tokens_to_df(tokens_title2):
    title_cnt = Counter(tokens_title2)
    df_title_cnt = pd.DataFrame(pd.Series(title_cnt), columns=['Freq'])
    sorted_title_cnt = df_title_cnt.sort_values(by='Freq', ascending=False)
    return sorted_title_cnt

sub_list = ['IT_과학', '경제', '국제', '문화', '미분류', '사회', '스포츠','정치', '지역']
sub = st.selectbox('대분류를 선택하세요',
             options=sub_list,
                      index=None,
                      placeholder='대분류를 선택해주세요!',
                      label_visibility='collapsed')
def sub_to_bar(subject):
    if sub == subject:
        a = title_to_tokens(df, sub)
        b = tokens_to_df(a)
        st.bar_chart(b.iloc[:20], color='#ffaa00')

sub_to_bar('IT_과학')
sub_to_bar('경제')
sub_to_bar('국제')
sub_to_bar('문화')
sub_to_bar('미분류')
sub_to_bar('사회')
sub_to_bar('스포츠')
sub_to_bar('정치')
sub_to_bar('지역')
st.divider()

# 3. 경기도인구데이터에 대하여
# 1) 연도별 인구수에 대한 지도시각화
#    2007년, 2015년, 2017년 연도를 탭으로 제시
df2 = pd.read_excel('data/경기도인구데이터.xlsx', index_col='구분')
with open('data/경기도행정구역경계.json', encoding='utf-8') as f:
    geo_gg = json.loads(f.read())

st.subheader('경기도 인구데이터 지도시각화')
tab1, tab2, tab3 = st.tabs(['2007년', '2015년', '2017년'])

def draw_map(year):
    st.markdown(f'{year}년 인구데이터')
    map = folium.Map(location=[37.5666, 126.9782], zoom_start=8)
    folium.GeoJson(geo_gg).add_to(map)
    folium.Choropleth(geo_data=geo_gg,
                      data=df2[year],
                      coliumns=[df2.index, df2[year]],
                      key_on='feature.properties.name').add_to(map)
    st_folium(map, width=600, height=400)

with tab1:
    draw_map(2007)

with tab2:
    draw_map(2015)

with tab3:
    draw_map(2017)

