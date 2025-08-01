import streamlit as st

st.set_page_config(
    page_title="과학 실험 데이터 분석 앱",
    page_icon="🔬",
)

pages = {
    "메인 페이지": [
        st.Page("./pages/main_page.py", title="시작하기"),
    ],
    "실험 페이지": [
        st.Page("./pages/gravity.py", title="MBL 중력 가속도 측정"),
        st.Page("./pages/inertia.py", title="관성모멘트와 역학적 에너지 보존"),
        st.Page("./pages/pendulum.py", title="단진자 주기 측정"),
    ]
}

pg = st.navigation(pages)
pg.run()
