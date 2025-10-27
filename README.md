# 🧍‍♂️ Real-Time Posture Checker

A **real-time posture detection app** built with **OpenCV**, **MediaPipe**, and **Streamlit**.  
It uses your webcam to detect your body landmarks and determine whether you are sitting or standing with good posture.  
The app also detects when your lighting is too dark and gives you a helpful warning — without stopping the camera feed.

---

## 🚀 Features

- 🎥 Live camera feed with **pose landmark tracking**  
- 🧠 Calculates a **posture ratio** using the position of your nose and shoulders  
- ✅ Displays **“Good”** or **“Bad”** posture status in real time 
- ⚡ Built with **Streamlit** for an easy-to-use web interface  

---

## 🧩 How It Works

1. **MediaPipe Pose** detects 33 key body landmarks in real time.  
2. The app measures the vertical distance between your **nose** and **shoulders**,  
   normalized by the distance between your **shoulders**.  
3. This gives a **posture ratio** that adjusts for distance from the camera.  
4. If the ratio falls below a set threshold (default `0.75`), it’s labeled “Bad Posture.” 

---

## 🛠️ Installation

### 1. Clone the repository
```bash
git clone https://github.com/Jshepherd06/Posture-Checker.git
cd posture-checker
```

### 2. Install Dependencies
If you are using the provided pyproject.toml:
```bash
pip install .
```
or you can do it manually:
```bash
pip install streamlit opencv-python mediapipe numpy
```

## Usage
Open terminal or cd into PostureChecker/ folder then run the streamlit app:
```bash
streamlit run interface.py
```
This will open a browser tab with the application


## 🧠 Dependencies

OpenCV
 – Real-time camera use

MediaPipe
 – Human pose detection

Streamlit
 – Web UI framework

NumPy


## todo: 
  - improved posture analysis (posture analyzer class or model)
  - calibration
  - PoseDetector class
  - user interface

    a. set posture analysis sensitivity

    b. calibrate button

    c. run

    d. want it to be a gui (not terminal)

    e. warning settings
    
  - warning sound/popup
  - statistical analysis longer periods
    
