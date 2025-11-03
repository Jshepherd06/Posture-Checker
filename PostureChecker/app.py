import streamlit as st
import cv2
import mediapipe as mp
from PoseDetector import PoseDetector

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