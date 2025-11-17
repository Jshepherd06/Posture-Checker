#  Real-Time Posture Checker

A **real-time posture detection app** built with **OpenCV**, **MediaPipe**, and **PyQT**.  
It uses your webcam to detect your body landmarks and determine whether you are sitting or standing with good posture.

---

##  Features

-  Live camera feed with **pose landmark tracking**  
-  Calculates a **posture ratio** using the position of your nose and shoulders  
-  Displays **“Good”** or **“Bad”** posture status in real time 
-  UI made with PyQT with adjustable settings

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
pip install PyQt6 opencv-python mediapipe numpy pygame
```

## Usage
Open terminal or cd into pyqt/ folder then run the pyqt app:
```bash
python main.py
```
This will open the application


## 🧠 Dependencies

**OpenCV**
 – Real-time camera use

**MediaPipe**
 – Human pose detection

**PyQT**
 – UI framework

**NumPy**

**PyGame**
 – Audio handling


## todo: 
  - improve readme
  - replace streamlit app with pyqt app
  - warning sound/popup
  - statistical analysis longer periods
  - error handling
    
