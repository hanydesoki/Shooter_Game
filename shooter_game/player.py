import math

import pygame

from .entity import Entity
from .weapon import *
from .utils import get_direction

class Player(Entity):

    speed = 2

    max_recovery_frame = 60

    collision_damage = 1

    def __init__(self, x, y, hp = 1, weapon = None):
        super().__init__(x, y, hp, weapon)

        self.surf.fill("blue")
  

    def manage_inputs(self) -> None:

        key_pressed = pygame.key.get_pressed()
        mouse_pressed = pygame.mouse.get_pressed()

        if key_pressed[pygame.K_z]:
            self.y = max(self.y - self.speed, 0)
        if key_pressed[pygame.K_s]:
            self.y = min(self.y + self.speed, self.screen_height)
        if key_pressed[pygame.K_q]:
            self.x = max(self.x - self.speed, 0)
        if key_pressed[pygame.K_d]:
            self.x = min(self.x + self.speed, self.screen_width)

        if mouse_pressed[0]:
            x, y = get_direction(self.center, pygame.mouse.get_pos())

            self.fire((x, y))

    def update(self) -> None:
        super().update()
        # print(self.weapon.bullets)
        self.manage_inputs()

        