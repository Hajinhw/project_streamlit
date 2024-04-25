# 뉴스 데이터 kor_news_20240326.xlsx를 이용하여 스트림릿으로 구현하기
import pandas as pd
import streamlit as st
from konlpy.tag import Okt
from collections import Counter

# 1. 뉴스데이터를 dataframe으로 표시하기
st.subheader('뉴스데이터 dataframe')
df = pd.read_excel('data/kor_news_240326.xlsx')
st.dataframe(df.iloc[:100], hide_index=True)
st.divider()

# 2. 뉴스데이터의 url 컬럼을 실제 뉴스기사 페이지로 이동하도록 적절한 column configuration 사용
st.subheader('뉴스데이터 url 연결')
st.dataframe(df,
             column_config={
                 'URL' : st.column_config.LinkColumn(
                     help='news link!',
                     display_text='뉴스 본문 링크로 이동'
                 )
             })
st.divider()

# 3. 분류 컬럼 중 대분류 컬럼에 대한 빈도를 bar chart로 그리기
st.subheader('대분류 빈도 그래프')
df['대분류'] = df.분류.str.split('>').str[0]
# 대분류 빈도를 데이터프레임으로 저장
df2 = pd.DataFrame(df.대분류.value_counts())
# 빈도그래프
st.bar_chart(df2)
st.divider()

# 4. 제목 컬럼에 대하여 텍스트 전처리를 진행한 결과를 토대로
#    경제, 사회 분야의 빈도가 많은 주요 키워드 20위를 bar chart로 그리기
st.subheader('제목 키워드 Top20 빈도 그래프')
okt = Okt()

# 뉴스 제목 토큰화 함수
def title_to_tokens(df, sub):
    df_eco = df[df['대분류']==sub]
    df_title = list(df_eco['제목'].values)
    tokens_df = [okt.nouns(title) for title in df_title]
    tokens_title = sum(tokens_df, [])
    tokens_title2 = [token for token in tokens_title if len(token) > 1]
    return tokens_title2

# 제목 키워드 빈도를 데이터프레임으로 저장하는 함수
def tokens_to_df(tokens_title2):
    title_cnt = Counter(tokens_title2)
    df_title_cnt = pd.DataFrame(pd.Series(title_cnt), columns=['Freq'])
    sorted_title_cnt = df_title_cnt.sort_values(by='Freq', ascending=False)
    return sorted_title_cnt

# 빈도그래프
c1, c2 = st.columns(2)

with c1:
    st.markdown('경제 분야')
    a = title_to_tokens(df, '경제')
    b = tokens_to_df(a)
    st.bar_chart(b.iloc[:20], color='#ffaa00')


with c2:
    st.markdown('사회 분야')
    c = title_to_tokens(df, '사회')
    d = tokens_to_df(c)
    st.bar_chart(d.iloc[:20], color='#ffaa0088')

