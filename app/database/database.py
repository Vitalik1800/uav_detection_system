import sqlite3

class Database:

    def __init__(self):

        self.connection = sqlite3.connect(
            "uav_detection.db"
        )

        self.cursor = self.connection.cursor()

        self.create_tables()

    def create_tables(self):

        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS detections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                confidence REAL,
                object_class TEXT,
                screenshot_path TEXT
            )
        """)

        self.connection.commit()

    def close(self):

        self.connection.close()
