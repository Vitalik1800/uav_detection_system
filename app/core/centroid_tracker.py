from collections import OrderedDict

import numpy as np


class CentroidTracker:

    def __init__(
        self,
        max_disappeared=40,
        max_distance=300
    ):

        self.next_object_id = 0

        self.objects = OrderedDict()

        self.disappeared = OrderedDict()

        self.max_disappeared = max_disappeared

        self.max_distance = max_distance

    def register(
        self,
        centroid
    ):

        print(
            f"[REGISTER] "
            f"NEW ID {self.next_object_id} "
            f"CENTROID {centroid}"
        )

        self.objects[
            self.next_object_id
        ] = centroid

        self.disappeared[
            self.next_object_id
        ] = 0

        self.next_object_id += 1

    def deregister(
        self,
        object_id
    ):

        print(
            f"[DEREGISTER] "
            f"REMOVE ID {object_id}"
        )

        del self.objects[object_id]

        del self.disappeared[object_id]

    def reset(self):

        print(
            "\n"
            "=====================\n"
            "TRACKER RESET\n"
            "=====================\n"
        )

        self.objects = OrderedDict()

        self.disappeared = OrderedDict()

        self.next_object_id = 0

    def update(
        self,
        rects
    ):

        print("\n========== TRACK UPDATE ==========")

        print(f"RECTS: {len(rects)}")

        # NO DETECTIONS
        if len(rects) == 0:

            print("NO DETECTIONS")

            remove_ids = []

            for object_id in list(
                self.disappeared.keys()
            ):

                self.disappeared[
                    object_id
                ] += 1

                print(
                    f"ID {object_id} "
                    f"DISAPPEARED "
                    f"{self.disappeared[object_id]}"
                )

                if (
                    self.disappeared[object_id]
                    > self.max_disappeared
                ):

                    remove_ids.append(
                        object_id
                    )

            for object_id in remove_ids:

                self.deregister(
                    object_id
                )

            return self.objects

        # INPUT CENTROIDS
        input_centroids = np.zeros(
            (len(rects), 2),
            dtype="int"
        )

        for (
            i,
            (x1, y1, x2, y2)
        ) in enumerate(rects):

            cX = int((x1 + x2) / 2.0)

            cY = int((y1 + y2) / 2.0)

            input_centroids[i] = (
                cX,
                cY
            )

            print(
                f"INPUT {i}: "
                f"{(cX, cY)}"
            )

        # FIRST OBJECTS
        if len(self.objects) == 0:

            print("NO EXISTING OBJECTS")

            for i in range(
                len(input_centroids)
            ):

                self.register(
                    input_centroids[i]
                )

            return self.objects

        object_ids = list(
            self.objects.keys()
        )

        object_centroids = list(
            self.objects.values()
        )

        print(f"TRACKED IDS: {object_ids}")

        print(
            f"TRACKED CENTROIDS: "
            f"{object_centroids}"
        )

        # DISTANCE MATRIX
        D = np.linalg.norm(

            np.array(object_centroids)[
                :, np.newaxis
            ]
            - input_centroids,

            axis=2
        )

        print("\nDISTANCE MATRIX:")
        print(D)

        rows = D.min(axis=1).argsort()

        cols = D.argmin(axis=1)[rows]

        used_rows = set()

        used_cols = set()

        # UPDATE OBJECTS
        for (row, col) in zip(
            rows,
            cols
        ):

            if row in used_rows:
                continue

            if col in used_cols:
                continue

            distance = D[row, col]

            print(
                f"\nMATCH:"
                f" ROW={row}"
                f" COL={col}"
                f" DIST={distance}"
            )

            if distance > self.max_distance:

                print(
                    "TOO FAR -> SKIP"
                )

                continue

            object_id = object_ids[row]

            print(
                f"UPDATE ID {object_id}"
            )

            self.objects[
                object_id
            ] = input_centroids[col]

            self.disappeared[
                object_id
            ] = 0

            used_rows.add(row)

            used_cols.add(col)

        # UNUSED ROWS
        unused_rows = set(
            range(D.shape[0])
        ).difference(used_rows)

        # UNUSED COLS
        unused_cols = set(
            range(D.shape[1])
        ).difference(used_cols)

        print(f"UNUSED ROWS: {unused_rows}")

        print(f"UNUSED COLS: {unused_cols}")

        # DISAPPEARED OBJECTS
        for row in unused_rows:

            object_id = object_ids[row]

            self.disappeared[
                object_id
            ] += 1

            print(
                f"ID {object_id} "
                f"MISSED "
                f"{self.disappeared[object_id]}"
            )

            if (
                self.disappeared[object_id]
                > self.max_disappeared
            ):

                self.deregister(
                    object_id
                )

        # NEW OBJECTS
        for col in unused_cols:

            self.register(
                input_centroids[col]
            )

        print(
            f"ACTIVE OBJECTS: "
            f"{self.objects}"
        )

        return self.objects
