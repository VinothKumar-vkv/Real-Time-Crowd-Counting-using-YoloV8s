# 🔍 Real-Time Crowd Counting & Social Distancing Violation Detection

![App Preview](https://github.com/your-username/your-repo-name/assets/banner.gif)

> A real-time computer vision project using YOLOv8 and Streamlit to monitor crowd density, count people, and detect social distancing violations. Built with a focus on public safety, smart surveillance, and practical AI deployment.

---

## 🚀 Features

- 🧠 **Powered by YOLOv8** – Fast and accurate real-time object detection.
- 📷 **Live Webcam or Uploaded Video Input** – Choose your video source easily.
- 📊 **Real-Time Graphs** – Track people count and violations over time.
- 🧩 **Modular Design** – Easily extendable for new features (e.g., alerts, zone analysis).
- 💻 **Streamlit UI** – Clean, interactive and responsive interface.
- ⚙️ **Customizable Settings** – Adjust detection threshold and visualization overlays.

---

## 📸 Demo

https://user-images.githubusercontent.com/your-github-username/demo.gif

---

## 🧠 Tech Stack

| Tool           | Purpose                             |
|----------------|-------------------------------------|
| [YOLOv8](https://github.com/ultralytics/ultralytics) | Real-time object detection |
| OpenCV         | Image/Video processing              |
| Streamlit      | Web UI & dashboard framework        |
| Plotly         | Live visualizations and metrics     |
| Python         | Programming language                |

---

## 📁 Project Structure

├── app.py # Streamlit app
├── crowd_utils.py # Crowd detection logic (YOLOv8 + CV)
├── requirements.txt # Python dependencies
└── README.md # This file


---

## ⚙️ Installation & Setup

1. **Clone the repository**
bash
git clone https://github.com/VinothKumar-vkv/Real-Time-Crowd-Counting-using-YoloV8s
cd real-time-crowd-monitoring

2. Install dependencies
   pip install -r requirements.txt

3. Download YOLOv8 model

The app uses the yolov8s.pt model. Download from Ultralytics or run:
from ultralytics import YOLO
YOLO('yolov8s.pt')

4. 
