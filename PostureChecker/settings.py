import streamlit as st

def main():
    st.set_page_config(page_title="Settings", layout="centered")
    st.title("⚙️ Posture Detector Settings")

    if "pose_settings" not in st.session_state:
        st.session_state.pose_settings = {
            "posture_threshold": 0.75,
            "posture_strictness": 0.85,
            "warning_wait": 3,
            "calibration_duration": 3,
            "sound_enabled": True,
        }

    settings = st.session_state.pose_settings

    st.subheader("🧍 Posture Sensitivity Without Calibration")
    settings["posture_threshold"] = st.slider(
        "Threshold between good and bad posture",
        0.5, 1.0, settings["posture_threshold"], 0.01
    )

    st.subheader("🧍 Posture Strictness (% of ideal posture needed)")
    settings["posture_strictness"] = st.slider(
        "Posture sensitivity (% of baseline)",
        0.5, 1.0, settings["posture_strictness"], 0.01
    )

    st.subheader("🔊 Audio & Alerts")
    settings["warning_wait"] = st.slider(
        "Cooldown between warnings (seconds)",
        1, 10, settings["warning_wait"], 1
    )
    settings["sound_enabled"] = st.toggle("Enable warning sound", settings["sound_enabled"])

    st.subheader("🧠 Calibration")
    settings["calibration_duration"] = st.slider(
        "Calibration duration (seconds)",
        2, 10, settings["calibration_duration"], 1
    )

    st.success("Settings saved automatically!")

if __name__ == "__main__":
    main()