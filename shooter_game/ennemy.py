import pygame

from .entity import Entity
from .utils import get_direction


class Ennemy(Entity):

    name = "Ennemy"
    speed = 1
    default_hp = 2

    def __init__(self, player, x, y, hp = 1, weapon = None):
        super().__init__(x, y, hp, weapon)
        self.surf.fill("red")

        self.player = player

    def move_to_player(self) -> None:
        player_direction = get_direction((self.center), (self.player.center))

        self.x += player_direction[0] * self.speed
        self.y += player_direction[1] * self.speed

        self.fire(player_direction)

        # print(
        #     player_direction, 
        #     (player_direction[0] * self.speed, player_direction[1] * self.speed), 
        #     (self.x, self.y),
        # )

    def update(self) -> None:
        super().update()
        self.move_to_player()



class Boss(Ennemy):
    name = "Boss"

    default_hp = 20

    def __init__(self, player, x, y, hp=1, weapon=None):
        super().__init__(player, x, y, hp, weapon)

        self.surf = pygame.Surface((50, 50))
        self.rect = self.surf.get_rect(center=(x, y))

        self.surf.fill([180, 0, 0])




        




    