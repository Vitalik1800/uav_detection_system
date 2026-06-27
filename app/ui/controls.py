import pygame
import cv2

from app.core.config import *


class VideoControls:

    def __init__(self):

        self.font = pygame.font.SysFont(
            "Arial",
            24
        )

        self.paused = False

        panel_x = VIDEO_WIDTH

        button_width = 120
        button_height = 60

        self.play_button = pygame.Rect(
            panel_x + 40,
            520,
            button_width,
            button_height
        )

        self.pause_button = pygame.Rect(
            panel_x + 240,
            520,
            button_width,
            button_height
        )

        self.restart_button = pygame.Rect(
            panel_x + 40,
            610,
            320,
            60
        )

        self.timeline_rect = pygame.Rect(
            panel_x + 40,
            690,
            320,
            12
        )

    def draw(
        self,
        screen
    ):

        pygame.draw.rect(
            screen,
            (0, 180, 0),
            self.play_button,
            border_radius=14
        )

        pygame.draw.rect(
            screen,
            (200, 130, 0),
            self.pause_button,
            border_radius=14
        )

        pygame.draw.rect(
            screen,
            (0, 120, 255),
            self.restart_button,
            border_radius=14
        )

        self.draw_centered_text(
            screen,
            "PLAY",
            self.play_button
        )

        self.draw_centered_text(
            screen,
            "PAUSE",
            self.pause_button
        )

        self.draw_centered_text(
            screen,
            "RESTART",
            self.restart_button
        )

    def draw_centered_text(
        self,
        screen,
        text,
        rect
    ):

        rendered_text = self.font.render(
            text,
            True,
            (255, 255, 255)
        )

        text_rect = rendered_text.get_rect(
            center=rect.center
        )

        screen.blit(
            rendered_text,
            text_rect
        )

    def handle_click(
        self,
        mouse_pos,
        video
    ):

        if not video:

            return

        try:

            # PLAY
            if self.play_button.collidepoint(mouse_pos):

                print("[ACTION] PLAY")

                self.paused = False

                print("[STATE] PLAYING")

            # PAUSE
            elif self.pause_button.collidepoint(mouse_pos):

                print("[ACTION] PAUSE")

                self.paused = True

                print("[STATE] PAUSED")

            # RESTART
            elif self.restart_button.collidepoint(mouse_pos):

                print("[ACTION] RESTART")

                self.paused = True

                video.cap.set(
                    cv2.CAP_PROP_POS_FRAMES,
                    0
                )

                print("[STATE] RESTARTED")

        except Exception as error:

            print(
                f"[CONTROLS ERROR] {error}"
            )

    def handle_timeline_click(
        self,
        mouse_pos,
        video
    ):

        if not video:

            return

        try:

            if self.timeline_rect.collidepoint(mouse_pos):

                relative_x = (
                    mouse_pos[0]
                    - self.timeline_rect.x
                )

                percent = (
                    relative_x
                    / self.timeline_rect.width
                )

                total_frames = int(
                    video.cap.get(
                        cv2.CAP_PROP_FRAME_COUNT
                    )
                )

                target_frame = int(
                    percent * total_frames
                )

                print(
                    f"[TIMELINE] {target_frame}"
                )

                self.paused = True

                video.cap.set(
                    cv2.CAP_PROP_POS_FRAMES,
                    target_frame
                )

        except Exception as error:

            print(
                f"[TIMELINE ERROR] {error}"
            )

    def draw_timeline(
        self,
        screen,
        current_frame,
        total_frames
    ):

        pygame.draw.rect(
            screen,
            (70, 70, 70),
            self.timeline_rect,
            border_radius=6
        )

        if total_frames <= 0:

            return

        progress_width = int(
            (
                current_frame
                / total_frames
            )
            * self.timeline_rect.width
        )

        progress_rect = pygame.Rect(
            self.timeline_rect.x,
            self.timeline_rect.y,
            progress_width,
            self.timeline_rect.height
        )

        pygame.draw.rect(
            screen,
            (0, 255, 120),
            progress_rect,
            border_radius=6
        )
