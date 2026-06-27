import cv2
import pygame
import time

from datetime import datetime

from app.ui.file_picker import select_video

from app.core.video_capture import VideoCapture
from app.core.detector import DroneDetector
from app.core.tracker import DroneTracker

from app.ui.window import UIWindow
from app.ui.hud import HUD
from app.ui.buttons import ButtonSystem
from app.ui.controls import VideoControls

from app.utils.logger import DetectionLogger
from app.utils.screenshot import ScreenshotSystem

from app.database.repository import DetectionRepository

from app.core.config import *

import numpy as np

def main():

    # INIT
    pygame.init()

    # SYSTEMS
    detector = DroneDetector()

    tracker = DroneTracker()

    window = UIWindow()

    recording = False

    video_writer = None

    hud = HUD()

    buttons = ButtonSystem()

    controls = VideoControls()

    logger = DetectionLogger()

    screenshot_system = ScreenshotSystem()

    repository = DetectionRepository()

    # VIDEO
    video = None

    # FPS
    prev_time = time.time()

    # FRAME COUNTER
    frame_count = 0

    # DETECTIONS
    detections = 0

    total_detections = 0

    # DETECTION COOLDOWN
    last_detection_time = 0

    DETECTION_COOLDOWN = 5

    # RESULTS
    results = []

    # FILTERED RESULTS
    filtered_results = []

    # FRAMES
    frame = None

    last_frame = None

    original_frame = None

    # FPS
    fps = 0

    # MAIN LOOP
    running = True

    while running:

        # EVENTS
        for event in pygame.event.get():

            # EXIT
            if event.type == pygame.QUIT:

                running = False

            # MOUSE
            if event.type == pygame.MOUSEBUTTONDOWN:

                mouse_pos = pygame.mouse.get_pos()

                # OPEN VIDEO
                if buttons.open_video_button.collidepoint(mouse_pos):

                    video_path = select_video()

                    if video_path:

                        # RELEASE OLD VIDEO
                        if video:

                            video.release()

                        # LOAD VIDEO
                        video = VideoCapture(video_path)

                        tracker.reset()

                        controls.paused = False

                        # RESET
                        results = []

                        filtered_results = []

                        detections = 0

                        total_detections = 0
                        
                        last_detection_time = 0

                        frame = None

                        last_frame = None

                        original_frame = None

                        frame_count = 0

                        print(f"VIDEO LOADED: {video_path}")

                # SAVE LOG
                elif buttons.save_log_button.collidepoint(mouse_pos):

                    logger.save_log(
                        detections,
                        int(fps)
                    )

                    print("LOG SAVED")

                # SCREENSHOT
                elif buttons.screenshot_button.collidepoint(mouse_pos):

                    if original_frame is not None:

                        screenshot_path = screenshot_system.save_screenshot(
                            original_frame
                        )

                        repository.save_detection(

                            timestamp=str(datetime.now()),

                            confidence=0.95,

                            object_class="manual_screenshot",

                            screenshot_path=screenshot_path
                        )

                        print("SCREENSHOT SAVED")

                # VIDEO CONTROLS
                else:

                    controls.handle_click(
                        mouse_pos,
                        video
                    )

                    # RESET AFTER RESTART
                    if (
                        controls.restart_button.collidepoint(
                            mouse_pos
                        )
                    ):

                        results = []

                        filtered_results = []

                        detections = 0

                # TIMELINE
                if controls.timeline_rect.collidepoint(mouse_pos):

                    if video:

                        relative_x = (
                            mouse_pos[0]
                            - controls.timeline_rect.x
                        )

                        percent = (
                            relative_x
                            / controls.timeline_rect.width
                        )

                        total_frames = int(
                            video.cap.get(
                                cv2.CAP_PROP_FRAME_COUNT
                            )
                        )

                        target_frame = int(
                            percent * total_frames
                        )

                        video.cap.set(
                            cv2.CAP_PROP_POS_FRAMES,
                            target_frame
                        )

            # KEYBOARD
            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_r:

                    recording = not recording

                    if recording:

                        fourcc = cv2.VideoWriter_fourcc(*"mp4v")

                        video_writer = cv2.VideoWriter(
                            f"demo_{datetime.now().strftime('%Y%m%d_%H%M%S')}.mp4",
                            fourcc,
                            FPS,
                            (WINDOW_WIDTH, WINDOW_HEIGHT)
                        )

                        print("VIDEO RECORDING STARTED")

                    else:

                        if video_writer:
                            video_writer.release()

                        video_writer = None

                        print("VIDEO RECORDING STOPPED")
                
                # NEXT FRAME
                if event.key == pygame.K_RIGHT:

                    if video:

                        controls.paused = True

                        frame = video.read()

                        if frame is not None:

                            last_frame = frame.copy()

        # BACKGROUND
        window.screen.fill((15, 15, 15))

        # NO VIDEO
        if video is None:

            font = pygame.font.SysFont(
                "Arial",
                42
            )

            text = font.render(
                "NO VIDEO LOADED",
                True,
                (255, 255, 255)
            )

            window.screen.blit(
                text,
                (260, 320)
            )

            buttons.draw_buttons(
                window.screen
            )

            pygame.display.update()

            continue

        # VIDEO READ
        if not controls.paused:

            frame = video.read()

            if frame is not None:

                last_frame = frame.copy()

            frame_count += 1

        else:

            frame = last_frame

        # EOF
        if frame is None:

            controls.paused = True

            controls.draw(
                window.screen
            )

            buttons.draw_buttons(
                window.screen
            )

            pygame.display.update()

            continue

        # COPY ORIGINAL
        original_frame = frame.copy()

        # RESIZE
        frame = cv2.resize(

            frame,

            (
                WINDOW_WIDTH - SIDEBAR_WIDTH,
                WINDOW_HEIGHT
            )
        )

        # DETECTION
        if frame_count % 2 == 0:

            results = detector.detect(frame)

        print(
            f"\nFRAME: {frame_count}"
        )

        # FILTERED DETECTIONS
        filtered_results = []

        detections = 0

        current_time = time.time()

        for result in results:

            valid_boxes = []

            boxes = result.boxes

            for box in boxes:

                confidence = float(box.conf[0])

                class_id = int(box.cls[0])

                class_name = detector.model.names[class_id]

                print(
                    f"CLASS={class_name} "
                    f"CONF={confidence:.2f}"
                )

                # ONLY DRONES
                if class_name != "drone":
                    continue

                # CONFIDENCE FILTER
                if confidence < 0.45:
                    continue

                # BOX COORDS
                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                width = x2 - x1

                height = y2 - y1

                print(
                    f"BOX={(x1,y1,x2,y2)} "
                    f"W={width} "
                    f"H={height} "
                    f"CONF={confidence:.2f}"
                )

                # AREA FILTER
                area = width * height

                if area < 100:
                    continue

                # HUGE OBJECT FILTER
                if width > 100000 or height > 100000:
                    continue

                # TINY OBJECT FILTER
                #if width < 10 or height < 10:
                #    continue

                # ASPECT RATIO FILTER
                ratio = width / max(height, 1)

                if ratio > 4:
                    continue

                # VALID DETECTION
                valid_boxes.append(box)

                detections += 1

                # AUTO SAVE
                if (
                    current_time - last_detection_time
                    > DETECTION_COOLDOWN
                ):

                    screenshot_path = screenshot_system.save_screenshot(
                        original_frame
                    )

                    repository.save_detection(

                        timestamp=str(datetime.now()),

                        confidence=confidence,

                        object_class=class_name,

                        screenshot_path=screenshot_path
                    )

                    print(
                        f"DRONE DETECTED | "
                        f"CONF: {confidence:.2f}"
                    )

                    total_detections += 1

                    last_detection_time = current_time

            # SAVE FILTERED
            if len(valid_boxes) > 0:

                result.boxes = valid_boxes

                print(
                    f"VALID DRONE | "
                    f"CONF={confidence:.2f} "
                    f"BOX={(x1, y1, x2, y2)}"
                )

                filtered_results.append(result)

        # TRACKING ONLY FILTERED
        frame = tracker.draw_detections(
            frame,
            filtered_results
        )

        # FPS
        current_fps_time = time.time()

        delta_time = current_fps_time - prev_time

        fps = int(
            1 / max(delta_time, 0.0001)
        )

        prev_time = current_fps_time

        # CV2 -> RGB
        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        # SURFACE
        frame_surface = pygame.surfarray.make_surface(
            frame.swapaxes(0, 1)
        )

        # DRAW VIDEO
        window.screen.blit(
            frame_surface,
            (0, 0)
        )

        # HUD
        hud.draw(

            window.screen,

            fps,

            total_detections,

            detector.device
        )

        if recording:

            font = pygame.font.SysFont(
                "Arial",
                28,
                bold=True
            )

            rec_text = font.render(
                "REC",
                True,
                (255, 0, 0)
            )

            window.screen.blit(
                rec_text,
                (20, 60)
            )

        # BUTTONS
        buttons.draw_buttons(
            window.screen
        )

        # CONTROLS
        controls.draw(
            window.screen
        )

        # TIMELINE
        current_frame = int(
            video.cap.get(
                cv2.CAP_PROP_POS_FRAMES
            )
        )

        total_frames = int(
            video.cap.get(
                cv2.CAP_PROP_FRAME_COUNT
            )
        )

        controls.draw_timeline(

            window.screen,

            current_frame,

            total_frames
        )

        if recording and video_writer:

            frame_record = pygame.surfarray.array3d(
                window.screen
            )

            frame_record = np.transpose(
                frame_record,
                (1, 0, 2)
            )

            frame_record = cv2.cvtColor(
                frame_record,
                cv2.COLOR_RGB2BGR
            )

            video_writer.write(
                frame_record
            )

        # UPDATE
        window.update()

    # RELEASE
    if video:

        video.release()

    if video_writer:

        video_writer.release()

    pygame.quit()

    cv2.destroyAllWindows()


if __name__ == "__main__":

    main()
