import math

# import pygame

# from pg_utils import ScreenEvents

from .bullet import Bullet


class Weapon:

    speed = 1
    mag_size = 1
    fire_rate = 30
    damage = 1
    bullet_hp = 1

    def __init__(self, owner) -> None:
        self.owner = owner

        self.bullets = self.mag_size
        self.hp = self.bullet_hp
        self.frame_count: int = 0
        

    def fire(self, direction: tuple[float, float]) -> None:
        if self.bullets and self.frame_count == 0:
            self.bullets = max(self.bullets - 1, 0)
            self.spawn_bullets(direction)
            self.frame_count = self.fire_rate

    def spawn_bullets(self, direction: tuple[float, float]) -> list[Bullet]:
        bullet = Bullet(
            self.owner,
            self.owner.x,
            self.owner.y,
            direction[0] * self.speed,
            direction[1] * self.speed,
            self.damage,
            self.hp
        )

        return [bullet]

    def update(self) -> None:
        self.frame_count = max(self.frame_count - 1, 0)


class Pistol(Weapon):
    speed = 3
    mag_size = 30
    fire_rate = 30
    damage = 1
    bullet_hp = 1

    name = "Pistol"

class Magnum(Weapon):
    speed = 5
    mag_size = 10
    fire_rate = 60
    damage = 2
    bullet_hp = 3

    name = "Magnum"


class AssaultRifle(Weapon):
    speed = 5
    mag_size = 200
    fire_rate = 5
    damage = 1
    bullet_hp = 1

    name = "Assault rifle"


class Shotgun(Weapon):
    speed = 4
    mag_size = 12
    fire_rate = 120
    damage = 2
    bullet_hp = 1

    name = "Shotgun"

    def spawn_bullets(self, direction: tuple[float, float]) -> list[Bullet]:

        spread_angle = math.radians(20) # Deg

        main_angle = math.atan2(direction[1], direction[0])

        start_angle = main_angle - spread_angle / 2

        number_shots = 3

        bullets = []

        for i in range(number_shots):
            
            angle = start_angle + i * spread_angle / number_shots

            dirx = math.cos(angle)
            diry = math.sin(angle)

            bullet = Bullet(
                self.owner,
                self.owner.x,
                self.owner.y,
                dirx * self.speed,
                diry * self.speed,
                self.damage,
                self.hp
            )

            bullets.append(bullet)

        

        return bullets





        

