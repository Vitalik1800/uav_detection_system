from app.database.database import Database

class DetectionRepository:

    def __init__(self):

        self.db = Database()

    def save_detection(
        self,
        timestamp,
        confidence,
        object_class,
        screenshot_path
    ):

        self.db.cursor.execute("""
            INSERT INTO detections (
                timestamp,
                confidence,
                object_class,
                screenshot_path
            )

            VALUES (?, ?, ?, ?)
        """, (
            timestamp,
            confidence,
            object_class,
            screenshot_path
        ))

        self.db.connection.commit()
