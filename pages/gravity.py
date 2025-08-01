import streamlit as st
import numpy as np

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
    return representative_value, uncertainty

st.header('MBL 중력 가속도 측정')
st.markdown('---')

# 두 개의 컬럼을 사용하여 레이아웃을 분할.
#한쪽에서 경사각 설정하고 한쪽에서 값 입력후 밑에서 결과 값을 출력되는 구조로 
col1, col2 = st.columns([1, 2])

with col1:
    st.subheader('1. 경사각 선택')
    theta_deg = st.selectbox(
        '측정 각도를 선택하세요:',
        options=[10, 20, 30],
        key="selectbox_theta"
    )
    st.info(f"선택된 경사각: {theta_deg}°")

with col2:
    st.subheader('2. 가속도(a) 데이터 입력')
    st.write(f"선택한 경사각에 대한 가속도 측정값 5개를 입력하세요.")
    default_data = {
        '가속도($m/s^2$)': [0.0, 0.0, 0.0, 0.0, 0.0]
    }
    df_edited = st.data_editor(default_data, num_rows='dynamic')

# "분석" 버튼을 페이지 중앙에 배치
st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
if st.button('결과 분석', type="primary"):
    st.markdown("</div>", unsafe_allow_html=True)
    
    acceleration_data = df_edited['가속도($m/s^2$)']
    filtered_data = [val for val in acceleration_data if val != 0.0]

    if len(filtered_data) >= 1:
        st.markdown('---')
        st.subheader('분석 결과')

        representative_accel, accel_uncertainty = calculate_uncertainty(filtered_data)
        
        col_res1, col_res2, col_res3 = st.columns(3)
        
        with col_res1:
            st.metric(label="가속도 (a) 대표값", value=f"{representative_accel:.4f} m/s²", delta=f"±{accel_uncertainty}")
        
        theta_rad = np.deg2rad(theta_deg)
        experimental_g = representative_accel / np.sin(theta_rad)
        
        with col_res2:
            st.metric(label="실험 중력 가속도 (g)", value=f"{experimental_g:.4f} m/s²")
        
        theoretical_g = 9.81
        error_rate = abs((theoretical_g - experimental_g) / theoretical_g) * 100

        with col_res3:
            st.metric(label="오차율", value=f"{error_rate:.2f} %")
        
        # 오차율 수식 표시하는 부분(어케할지 모르겠음 나중에 보고 없애던가 해야할듯)
        st.markdown(f"""
        ---
        <h4 style="text-align: center;">오차율 계산 수식</h4>
        
        $
        \\text{{오차율}} = \\left| \\frac{{{theoretical_g} - {experimental_g:.4f}}}{{{theoretical_g}}} \\right| \\times 100 = {error_rate:.2f} \\%
        $
        """, unsafe_allow_html=True)
    
    else:
        st.error("가속도 측정값을 1개 이상 입력해주세요.")
else:
    st.markdown("</div>", unsafe_allow_html=True)

#이게
#되네