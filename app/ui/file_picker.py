from tkinter import Tk
from tkinter.filedialog import askopenfilename

def select_video():

    root = Tk()

    root.withdraw()

    file_path = askopenfilename(
        title="Select UAV Video",
        filetypes=[
            ("MP4 files", "*.mp4"),
            ("AVI files", "*.avi")
        ]
    )

    return file_path
