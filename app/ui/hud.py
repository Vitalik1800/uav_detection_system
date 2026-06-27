import pygame

from app.core.config import (
    VIDEO_WIDTH,
    SIDEBAR_WIDTH,
    WINDOW_HEIGHT
)

class HUD:

    def __init__(self):

        self.font = pygame.font.SysFont(
            "Arial",
            24
        )

        self.big_font = pygame.font.SysFont(
            "Arial",
            32,
            bold=True
        )

    def draw(
        self,
        screen,
        fps,
        detections,
        device,
        status="ACTIVE"
    ):

        panel_x = 1040

        # SIDEBAR
        pygame.draw.rect(
            screen,
            (20, 20, 20),
            (
                panel_x,
                0,
                SIDEBAR_WIDTH,
                WINDOW_HEIGHT
            )
        )

        # TITLE
        title = self.big_font.render(
            "UAV MONITOR",
            True,
            (0, 255, 0)
        )

        screen.blit(title, (panel_x + 40, 30))

        # STATUS
        status_text = self.font.render(
            f"STATUS: {status}",
            True,
            (0, 255, 0)
        )

        screen.blit(status_text, (panel_x + 40, 110))

        # DEVICE
        device_text = self.font.render(
            f"DEVICE: {device.upper()}",
            True,
            (255, 255, 255)
        )

        screen.blit(device_text, (panel_x + 40, 160))

        # FPS
        fps_text = self.font.render(
            f"FPS: {fps}",
            True,
            (255, 255, 255)
        )

        screen.blit(fps_text, (panel_x + 40, 210))

        # DETECTIONS
        detection_text = self.font.render(
            f"DETECTIONS: {detections}",
            True,
            (255, 70, 70)
        )

        screen.blit(detection_text, (panel_x + 40, 260))
