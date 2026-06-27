import cv2


class KalmanTracker:

    def __init__(self):

        self.kalman = cv2.KalmanFilter(4, 2)

        self.kalman.measurementMatrix = \
            cv2.setIdentity(
                self.kalman.measurementMatrix
            )

        self.kalman.transitionMatrix = np.array([
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], np.float32)
        
    def predict(self):

        prediction = self.kalman.predict()

        return prediction

    def correct(self, x, y):

        measured = \
            cv2.UMat(
                2,
                1,
                cv2.CV_32F
            )

        measured.get()[0] = x
        measured.get()[1] = y

        self.kalman.correct(measured)
