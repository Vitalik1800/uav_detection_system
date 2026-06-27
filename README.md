# 🚁 UAV Detection System using YOLOv8

![Python](https://img.shields.io/badge/Python-3.12-blue?logo=python)
![YOLOv8](https://img.shields.io/badge/YOLOv8-Ultralytics-green)
![PyTorch](https://img.shields.io/badge/PyTorch-Deep%20Learning-red?logo=pytorch)
![OpenCV](https://img.shields.io/badge/OpenCV-Computer%20Vision-blue?logo=opencv)
![SQLite](https://img.shields.io/badge/SQLite-Database-blue)
![Pygame](https://img.shields.io/badge/Pygame-GUI-darkgreen)
![License](https://img.shields.io/badge/License-MIT-yellow)

Desktop application for **real-time UAV (drone) detection** using **YOLOv8**, **Computer Vision**, and **Object Tracking**.

The system analyzes video streams, detects unmanned aerial vehicles, assigns unique IDs to detected objects, stores detection history in an SQLite database, automatically saves screenshots, and provides a convenient graphical user interface.

---

# 🔗 Repository

**GitHub Repository**

https://github.com/Vitalik1800/uav_detection_system

---

# 🚀 Features

## 🎥 Video Processing

- Open video files
- Frame-by-frame processing
- Playback controls
- Timeline navigation
- Pause / Resume / Restart

---

## 🚁 UAV Detection

- YOLOv8 object detection
- Real-time inference
- Confidence filtering
- Bounding box visualization
- Detection statistics

---

## 🎯 Object Tracking

- Centroid Tracker
- Persistent object IDs
- Stable tracking across frames
- Multi-object support

---

## 📷 Automatic Screenshot System

- Automatic screenshot saving
- Manual screenshot capture
- Timestamp generation
- Detection image archive

---

## 🗄 Database

- SQLite storage
- Detection history
- Timestamp logging
- Confidence values
- Screenshot path storage

---

## 🖥 Desktop Application

- Pygame graphical interface
- Live video preview
- FPS counter
- Detection counter
- CPU/GPU information
- Event logging

---

# 🛠 Tech Stack

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| YOLOv8 (Ultralytics) | Object Detection |
| PyTorch | Deep Learning |
| OpenCV | Computer Vision |
| Pygame | Desktop GUI |
| SQLite | Database |
| NumPy | Numerical Computing |

---

# 📂 Project Structure

```text
uav_detection_system/
│
├── app/
│   ├── core/
│   ├── ui/
│   ├── database/
│   ├── utils/
│   └── models/
│
├── screenshots/
├── dataset/
├── videos/
│
├── main.py
├── requirements.txt
└── README.md
