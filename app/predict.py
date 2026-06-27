from ultralytics import YOLO

model = YOLO(
    "runs/detect/uav_detector_fast/weights/best.pt"
)

model.predict(
    source="videos/test_video.mp4",

    conf=0.3,

    save=True,

    imgsz=416
)
