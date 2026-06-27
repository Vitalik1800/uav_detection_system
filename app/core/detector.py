from ultralytics import YOLO

import torch


class DroneDetector:

    def __init__(self):

        self.device = "cuda" if torch.cuda.is_available() else "cpu"

        print(f"DEVICE: {self.device}")

        self.model = YOLO("app/models/best.pt")

        self.model.to(self.device)

        print("MODEL CLASSES:")
        print(self.model.names)

    def detect(self, frame):

        results = self.model(

            frame,

            imgsz=640,

            conf=0.45,

            device=self.device,

            verbose=False
        )

        return results
