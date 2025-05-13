from typing import Callable

import pygame

from pg_utils import ScreenEvents


class PickUp(ScreenEvents):

    def __init__(self, x: int, y: int):
        super().__init__()

        self.surf = pygame.Surface((40, 30))
        self.surf.fill("white")

        self.rect = self.surf.get_rect(center=(x, y))

    def draw(self) -> None:
        self.screen.blit(self.surf, self.rect)

class WeaponPickups(PickUp):

    def __init__(self, x, y, weapon):
        super().__init__(x, y)

        self.weapon = weapon