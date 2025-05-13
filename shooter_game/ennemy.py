from .entity import Entity
from .utils import get_direction


class Ennemy(Entity):

    def __init__(self, player, x, y, pv = 1, weapon = None):
        super().__init__(x, y, pv, weapon)
        self.surf.fill("red")

        self.player = player

        self.speed = 1

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


