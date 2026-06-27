import cv2
import os
from datetime import datetime


class ScreenshotSystem:

    def __init__(self):

        self.output_dir = "screenshots"

        os.makedirs(
            self.output_dir,
            exist_ok=True
        )

    def save_screenshot(
        self,
        frame
    ):

        timestamp = datetime.now().strftime(
            "%Y%m%d_%H%M%S"
        )

        filename = os.path.join(
            self.output_dir,
            f"uav_{timestamp}.jpg"
        )

        success = cv2.imwrite(
            filename,
            frame
        )

        if success:
            print(f"SCREENSHOT SAVED: {filename}")
        else:
            print("SCREENSHOT ERROR")

        return filename
