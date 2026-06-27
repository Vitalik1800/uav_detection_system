from datetime import datetime


class DetectionLogger:

    def save_log(
        self,
        drone_count,
        fps
    ):

        timestamp = datetime.now().strftime(
            "%Y-%m-%d %H:%M:%S"
        )

        log_text = (
            f"[{timestamp}] "
            f"Drones: {drone_count} | "
            f"FPS: {fps}\n"
        )

        with open(
            "detection_log.txt",
            "a",
            encoding="utf-8"
        ) as file:

            file.write(log_text)

        print("LOG SAVED")
