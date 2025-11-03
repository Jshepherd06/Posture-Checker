import streamlit as st
import cv2
import mediapipe as mp
from PoseDetector import PoseDetector

# Use Streamlit session state to persist settings between pages
if "pose_settings" not in st.session_state:
    st.session_state.pose_settings = {
        "posture_threshold": 0.75,
        "posture_strictness": 0.85,
        "warning_wait": 3,
        "calibration_duration": 3,
        "sound_enabled": True,
    }

Homepage = st.Page(
    "Homepage.py", 
    title="Home", 
    icon=":material/home:"
)

PoseDetector = st.Page(
    "PoseDetector.py",
    title="Pose Detector",
    icon=":material/healing:",
)

Statistics = st.Page(
    "stats.py",
    title="Statistics",
    icon=":material/healing:"
)

#use streamlit navigation and pages to go to posture detector
page_dict = {}
page_dict["Home"] = [Homepage]
page_dict["Pose Detector"] = [PoseDetector]
page_dict["Settings"] = [st.Page("settings.py", title="Settings", icon=":material/settings:")]
page_dict["Statistics"] = [Statistics]
pg = st.navigation(page_dict)
pg.run()