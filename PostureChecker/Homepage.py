import streamlit as st

st.header("Welcome!")
st.title("Posture Checker")

if st.button("Get Started"):
    st.switch_page("PoseDetector.py")