import pygame

from pg_utils import ScreenEvents

from .layout import Layout
from .settings import SCREEN_SIZE, FPS


def run_game() -> None:
    
    pygame.init()

    pygame.display.set_mode(SCREEN_SIZE)

    clock: pygame.time.Clock = pygame.time.Clock()

    layout: Layout = Layout()

    run_loop: bool = True


    while run_loop:

        all_events: list[pygame.event.Event] = pygame.event.get()

        for event in all_events:
            if event.type == pygame.QUIT:
                run_loop = False

        ScreenEvents.update_events(all_events)

        # Game code here

        layout.update()

        pygame.display.update()

        clock.tick(FPS)