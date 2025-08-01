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

st.header('단진자 주기 측정')
st.markdown('---')

col1, col2 = st.columns(2)

with col1:
    st.subheader('1. 진자 정보 입력')
    l_pendulum = st.number_input('진자의 길이(l)를 입력하세요 (m):', min_value=0.01, value=1.0, step=0.01, key="length_input")
    amplitude = st.number_input('진자의 진폭(각도)을 입력하세요 (°):', min_value=0.0, value=5.0, step=1.0, key="amplitude_input")
    mass_bob = st.number_input('추의 질량(m)을 입력하세요 (kg):', min_value=0.01, value=0.1, step=0.01, key="mass_input")
    
with col2:
    st.subheader('2. 10회 왕복 주기(10T) 데이터 입력')
    st.write(f"입력한 진자의 길이 **{l_pendulum}m**에 대한 10회 왕복 주기 측정값 5개를 입력하세요.")
    
    default_data = {
        '10회 왕복 주기($s$)': [0.0, 0.0, 0.0, 0.0, 0.0]
    }
    df_edited = st.data_editor(default_data, num_rows='dynamic', key="period_editor")

if st.button('분석'):
    data_10T = df_edited['10회 왕복 주기($s$)']
    filtered_data_10T = [val for val in data_10T if val != 0.0]
    
    if len(filtered_data_10T) >= 1:
        st.subheader('분석 결과')

        # 10회 주기값을 1회 주기로 변환하여 계산
        data_T = [val / 10 for val in filtered_data_10T]
        
        # 주기(T)의 대표값과 불확도 계산
        representative_T, t_uncertainty = calculate_uncertainty(data_T)
        
        g = 9.81
        T_theoretical = 2 * np.pi * np.sqrt(l_pendulum / g)
        
        error_rate = abs((T_theoretical - representative_T) / T_theoretical) * 100
        
        col_res1, col_res2, col_res3 = st.columns(3)
        with col_res1:
            st.metric(label=f"1회 주기(T) 실험값", value=f"{representative_T:.4f} s", delta=f"±{t_uncertainty:.4f}")
        with col_res2:
            st.metric(label=f"1회 주기(T) 이론값", value=f"{T_theoretical:.4f} s")
        with col_res3:
            st.metric(label=f"오차율", value=f"{error_rate:.2f} %")

        st.markdown(f"""
        ---
        <h4 style="text-align: center;">단진자 주기 수식 및 오차율</h4>
        
        $
        \\text{{실험값}} \, T = \\text{{평균}}\\left(\\frac{{\\text{{10회 왕복 주기}}}}{{10}}\\right) = {representative_T:.4f} \\pm {t_uncertainty:.4f}
        $
        
        $
        \\text{{이론값}} \, T_{{이론}} = 2\\pi \\sqrt{{\\frac{{l}}{{g}}}} = 2\\pi \\sqrt{{\\frac{{{l_pendulum}}}{{9.81}}}} = {T_theoretical:.4f} \\, s
        $
        
        $
        \\text{{오차율}} = \\left| \\frac{{\\text{{이론값}} - \\text{{실험값}}}}{{\\text{{이론값}}}} \\right| \\times 100 \\% = \\left| \\frac{{{T_theoretical:.4f} - {representative_T:.4f}}}{{{T_theoretical:.4f}}} \\right| \\times 100 = {error_rate:.2f} \\%
        $
        """, unsafe_allow_html=True)
        
    else:
        st.error("10회 왕복 주기 측정값을 1개 이상 입력해주세요.")