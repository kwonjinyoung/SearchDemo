import streamlit as st
import pandas as pd
import re

# 데이터 로드
@st.cache_data
def load_data():
    df = pd.read_csv('./데이터셋/2024년 지역축제 개최계획(수정).csv', encoding='utf-8')
    df.columns = df.iloc[0]
    df = df[1:]
    return df

df = load_data()

# 검색 함수 수정
def search_data(query):
    mask = df.apply(lambda row: row.astype(str).str.contains(query, case=False).any(), axis=1)
    return df[mask]

# 굵게 표시 및 밑줄 함수 수정
def highlight_match(text, query):
    pattern = re.compile(f'({re.escape(query)})', re.IGNORECASE)
    return pattern.sub(r'<u>**\1**</u>', str(text))

# 탭별 검색 함수
def general_search():
    query = st.session_state.general_query
    if query:
        # add_recent_search(query)
        results = search_data(query)
        display_results(results, query, "일반")

def embedding_search():
    query = st.session_state.embedding_query
    if query:
        # add_recent_search(query)
        # AI 임베딩 검색 로직 구현 필요
        st.warning("AI 임베딩 검색 기능은 아직 구현되지 않았습니다.")

def augmented_search():
    query = st.session_state.augmented_query
    if query:
        # add_recent_search(query)
        # AI 증강생성 검색 로직 구현 필요
        st.warning("AI 증강생성 검색 기능은 아직 구현되지 않았습니다.")

def display_results(results, query, search_type):
    if not results.empty:
        response = f"{search_type} 검색 결과: {len(results)}개의 축제를 찾았습니다.\n\n"
        for _, row in results.iterrows():
            festival_info = []
            if '축제명' in row:
                festival_info.append(highlight_match(row['축제명'], query))
            if '시군구명' in row:
                festival_info.append(highlight_match(row['시군구명'], query))
            if '개최기간' in row:
                festival_info.append(highlight_match(row['개최기간'], query))
            response += f"- {', '.join(festival_info)}\n"
    else:
        response = f"{search_type} 검색 결과가 없습니다."

    # 새로운 검색 결과를 세션 상태에 추가
    st.session_state.search_history.append(f"**{search_type} 검색어: {query}**\n\n{response}\n\n---\n\n")

# 세션 상태 초기화
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'general_query' not in st.session_state:
    st.session_state.general_query = ""
if 'embedding_query' not in st.session_state:
    st.session_state.embedding_query = ""
if 'augmented_query' not in st.session_state:
    st.session_state.augmented_query = ""
if 'current_tab' not in st.session_state:
    st.session_state.current_tab = "일반 검색"

# 최근 검색어 관련 함수 및 세션 상태 제거

# 사이드바에 세로로 나열된 탭 추가
with st.sidebar:
    st.title("축제 검색")
    
    st.session_state.current_tab = st.radio(
        "검색 유형 선택",
        ["일반 검색", "AI **임베딩** 검색", "AI **증강생성(RAG)** 검색"]
    )
    
    if st.session_state.current_tab == "일반 검색":
        st.text_input('일반 검색어를 입력하세요', key='general_query', on_change=general_search)
        st.button('일반 검색', on_click=general_search)
    
    elif st.session_state.current_tab == "AI **임베딩** 검색":
        st.text_input('AI 임베딩 검색어를 입력하세요', key='embedding_query', on_change=embedding_search)
        st.button('AI 임베딩 검색', on_click=embedding_search)
    
    elif st.session_state.current_tab == "AI **증강생성(RAG)** 검색":
        st.text_input('AI 증강생성 검색어를 입력하세요', key='augmented_query', on_change=augmented_search)
        st.button('AI 증강생성 검색', on_click=augmented_search)

# 메인 화면
st.title("축제 정보")

# 검색 결과 표시
st.subheader("검색 기록")
for result in reversed(st.session_state.search_history):
    st.markdown(result, unsafe_allow_html=True)

# 자동 스크롤
st.markdown("<script>window.scrollTo(0,0);</script>", unsafe_allow_html=True)

# 결과 상세 보기
# if st.button('전체 결과 보기'):
#     st.dataframe(df)