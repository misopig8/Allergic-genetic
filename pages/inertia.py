import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def calculate_uncertainty(data):
    if not data:
        return 0, 0
    representative_value = np.mean(data)
    max_diff = np.max(np.abs(data - representative_value))
    if max_diff == 0:
        uncertainty = 0
    else:
        power_of_10 = np.floor(np.log10(max_diff))
        uncertainty = round(max_diff, -int(power_of_10))
        
        if uncertainty < max_diff:
            uncertainty += 10**power_of_10
            
    return representative_value, uncertainty

st.header('관성모멘트와 역학적 에너지 보존')
st.markdown('---')

col1, col2 = st.columns(2)

with col1:
    st.subheader('1. 낙하 높이(h) 입력')
    h = st.number_input(
        '실험에서 측정한 낙하 높이(h)를 입력하세요 (m):',
        min_value=0.01,
        value=0.5,
        step=0.01,
        key="height_input"
    )
    st.subheader('2. 이론값 계산용 높이(H) 입력')
    H = st.number_input(
        '이론값 계산에 사용할 높이(H)를 입력하세요 (m):',
        min_value=0.01,
        value=0.5,
        step=0.01,
        key="theoretical_height_input"
    )

with col2:
    st.subheader('3. 수평 거리(L) 데이터 입력')
    st.write(f"입력한 높이 **{h}m**에 대한 수평 거리 측정값 5개를 입력하세요.")
    default_data = {
        '수평 거리(L)($m$)': [0.0, 0.0, 0.0, 0.0, 0.0]
    }
    df_edited = st.data_editor(default_data, num_rows='dynamic', key="distance_editor")

if st.button('분석'):
    l_data = df_edited['수평 거리(L)($m$)']
    filtered_l_data = [val for val in l_data if val != 0.0]
    
    if len(filtered_l_data) >= 1:
        st.subheader('분석 결과')

        representative_l, l_uncertainty = calculate_uncertainty(filtered_l_data)
        l_squared_data = [val**2 for val in filtered_l_data]
        representative_l_squared, l_squared_uncertainty = calculate_uncertainty(l_squared_data)

        k_experimental = np.mean([h / (val**2) for val in filtered_l_data])
        
        if H != 0:
            k_theoretical = 1 / (4 * H)
        else:
            k_theoretical = 0
            
        error_rate = abs((k_theoretical - k_experimental) / k_theoretical) * 100

        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            st.metric(label=f"L² 대표값", value=f"{representative_l_squared:.4f} m²", delta=f"±{l_squared_uncertainty:.4f}")
        with col_res2:
            st.metric(label=f"상수 k (실험값)", value=f"{k_experimental:.4f}")
        with col_res3:
            st.metric(label=f"오차율", value=f"{error_rate:.2f} %")

        # 수정된 부분: 중괄호 이스케이프 처리
        st.markdown(f"""
        ---
        <h4 style="text-align: center;">역학적 에너지 보존 수식 및 오차율</h4>
        
        $
        \\text{{실험값}} \, k = \\text{{평균}}\\left(\\frac{{h}}{{L^2}}\\right) = {k_experimental:.4f}
        $
        
        $
        \\text{{이론값}} \, k_{{이론}} = \\frac{{1}}{{4H}} = \\frac{{1}}{{4 \\times {H}}} = {k_theoretical:.4f}
        $
        
        $
        \\text{{오차율}} = \\left| \\frac{{\\text{{이론값}} - \\text{{실험값}}}}{{\\text{{이론값}}}} \\right| \\times 100 \\% = \\left| \\frac{{{k_theoretical:.4f} - {k_experimental:.4f}}}{{{k_theoretical:.4f}}} \\right| \\times 100 = {error_rate:.2f} \\%
        $
        """, unsafe_allow_html=True)
        
    else:
        st.error("수평 거리 측정값을 1개 이상 입력해주세요.")