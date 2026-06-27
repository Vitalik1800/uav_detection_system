import cv2

from app.core.centroid_tracker import CentroidTracker


class DroneTracker:

    def __init__(self):

        self.centroid_tracker = CentroidTracker()

    def reset(self):

        print(
            "\n"
            "=====================\n"
            "DRONE TRACKER RESET\n"
            "=====================\n"
        )

        self.centroid_tracker.reset()

    def draw_detections(
        self,
        frame,
        results
    ):

        print(
            "\n"
            "=====================================\n"
            "DRAW DETECTIONS\n"
            "====================================="
        )

        rects = []

        # =====================================
        # PARSE DETECTIONS
        # =====================================

        for result in results:

            boxes = result.boxes

            print(
                f"RESULT BOXES: {len(boxes)}"
            )

            for box in boxes:

                confidence = float(
                    box.conf[0]
                )

                class_id = int(
                    box.cls[0]
                )

                class_name = result.names[
                    class_id
                ]

                print(
                    f"\nCLASS={class_name} "
                    f"CONF={confidence:.2f}"
                )

                # ONLY DRONES
                if class_name != "drone":

                    print(
                        "SKIP: NOT DRONE"
                    )

                    continue

                # CONFIDENCE FILTER
                if confidence < 0.65:

                    print(
                        "SKIP: LOW CONFIDENCE"
                    )

                    continue

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                width = x2 - x1
                height = y2 - y1

                area = width * height

                print(
                    f"BOX={(x1, y1, x2, y2)} "
                    f"W={width} "
                    f"H={height} "
                    f"AREA={area}"
                )

                # FILTER SMALL OBJECTS
                if area < 80:

                    print(
                        "SKIP: SMALL AREA"
                    )

                    continue

                rects.append(
                    (x1, y1, x2, y2)
                )

                print(
                    f"VALID RECT -> "
                    f"{(x1, y1, x2, y2)}"
                )

        print(
            f"\nTOTAL VALID RECTS: "
            f"{len(rects)}"
        )

        # =====================================
        # UPDATE TRACKER
        # =====================================

        objects = self.centroid_tracker.update(
            rects
        )

        print(
            "\nTRACKER OBJECTS:"
        )

        for object_id, centroid in objects.items():

            print(
                f"ID={object_id} "
                f"CENTROID={centroid}"
            )

        print(
            f"TOTAL TRACKED: "
            f"{len(objects)}"
        )

        # =====================================
        # DRAW BOXES
        # =====================================

        for i, rect in enumerate(rects):

            x1, y1, x2, y2 = rect

            print(
                f"DRAW BOX {i}: "
                f"{rect}"
            )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

        # =====================================
        # DRAW IDS
        # =====================================

        for object_id, centroid in objects.items():

            cX, cY = centroid

            print(
                f"DRAW ID {object_id} "
                f"AT {(cX, cY)}"
            )

            cv2.circle(
                frame,
                (cX, cY),
                5,
                (0, 0, 255),
                -1
            )

            cv2.putText(
                frame,
                f"ID {object_id}",
                (cX - 20, cY - 15),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.7,
                (0, 255, 0),
                2
            )

        print(
            "=====================================\n"
        )

        return frame
