import streamlit as st
import time

with st.spinner('Wait for it...'):
    time.sleep(5)
st.balloons()
st.success('Done!')
st.snow()