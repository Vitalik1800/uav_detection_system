import pygame

from app.core.config import *

class UIWindow:

    def __init__(self):

        pygame.init()

        self.screen = pygame.display.set_mode(
            (
                WINDOW_WIDTH,
                WINDOW_HEIGHT
            )
        )

        pygame.display.set_caption(
            "UAV Detection System"
        )

        self.clock = pygame.time.Clock()

    def update(self):

        pygame.display.update()

        self.clock.tick(FPS)
        
