from .screen_events import ScreenEvents
from .vector import V2
from .mathematics import Mapper, distance_between_two_points, clamp_values
from .widgets import Text, Button


def get_basic_setup() -> str:
    return """
import pygame


pygame.init()

pygame.display.set_mode((500, 500))

clock = pygame.time.Clock()

run_loop = True


while run_loop:

    all_events = pygame.event.get()

    for event in all_events:
        if event.type == pygame.QUIT:
            run_loop = False

    # Game code here
    
    pygame.display.update()

    clock.tick(60)
    """
