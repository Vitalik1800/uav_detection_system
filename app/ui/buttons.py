import pygame

from app.core.config import *


class ButtonSystem:

    def __init__(self):

        self.font = pygame.font.SysFont(
            "Arial",
            26
        )

        panel_x = VIDEO_WIDTH

        self.button_width = 320
        self.button_height = 60

        # OPEN VIDEO
        self.open_video_button = pygame.Rect(
            panel_x + 40,
            250,
            self.button_width,
            self.button_height
        )

        # SAVE LOG
        self.save_log_button = pygame.Rect(
            panel_x + 40,
            340,
            self.button_width,
            self.button_height
        )

        # SCREENSHOT
        self.screenshot_button = pygame.Rect(
            panel_x + 40,
            430,
            self.button_width,
            self.button_height
        )

    def draw_button(
        self,
        screen,
        rect,
        color,
        text
    ):

        pygame.draw.rect(
            screen,
            color,
            rect,
            border_radius=18
        )

        text_surface = self.font.render(
            text,
            True,
            (255, 255, 255)
        )

        text_rect = text_surface.get_rect(
            center=rect.center
        )

        screen.blit(
            text_surface,
            text_rect
        )

    def draw_buttons(
        self,
        screen
    ):

        self.draw_button(
            screen,
            self.open_video_button,
            (0, 180, 120),
            "OPEN VIDEO"
        )

        self.draw_button(
            screen,
            self.save_log_button,
            (0, 120, 255),
            "SAVE LOG"
        )

        self.draw_button(
            screen,
            self.screenshot_button,
            (255, 70, 70),
            "SCREENSHOT"
        )
