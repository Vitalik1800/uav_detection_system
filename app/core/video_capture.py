import cv2


class VideoCapture:

    def __init__(
        self,
        source
    ):

        self.cap = cv2.VideoCapture(source)

        self.frame = None

        self.seeking = False

        # FIRST FRAME
        success, frame = self.cap.read()

        if success and frame is not None:

            self.frame = frame.copy()

    def read(self):

        if self.seeking:

            return self.frame

        success, frame = self.cap.read()

        if success and frame is not None:

            self.frame = frame.copy()

            return self.frame

        return None

    def set_frame_position(
        self,
        frame_number
    ):

        self.seeking = True

        self.cap.set(
            cv2.CAP_PROP_POS_FRAMES,
            frame_number
        )

        success, frame = self.cap.read()

        if success and frame is not None:

            self.frame = frame.copy()

        self.seeking = False

    def get_current_frame(self):

        return int(
            self.cap.get(
                cv2.CAP_PROP_POS_FRAMES
            )
        )

    def get_total_frames(self):

        return int(
            self.cap.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )

    def release(self):

        self.cap.release()
