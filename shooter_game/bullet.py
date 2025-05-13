import pygame

from pg_utils import ScreenEvents


class Bullet(ScreenEvents):

    all_bullets: list["Bullet"] = []

    all_owners = {}

    def __init__(self, owner, x: float, y: float, x_speed: float, y_speed: float, damage: int, hp: int = 1):
        super().__init__()

        self.owner = owner

        self.x = x
        self.y = y

        self.x_speed = x_speed
        self.y_speed = y_speed

        self.damage = damage

        self.hp = hp

        self.hitted_targets = []

        self.add_instance()

    def update_position(self) -> None:
        self.x += self.x_speed
        self.y += self.y_speed
    
    def draw(self) -> None:
        pygame.draw.circle(self.screen, "yellow", self.center, 3)

    
    def add_instance(self) -> None:
        self.all_bullets.append(self)
        
        if self.owner not in self.all_owners:
            self.all_owners[self.owner] = []

        self.all_owners[self.owner].append(self.owner)

    def remove_instance(self) -> None:
        if self in self.all_bullets:
            self.all_bullets.remove(self)
        
        if self in self.all_owners[self.owner]:
            self.all_owners[self.owner].remove(self)

    def is_inbound(self) -> bool:
        return (
            0 < self.x <= self.screen.get_width()
            and 
            0 < self.y <= self.screen.get_height()
        )
    
    def update(self) -> None:
        self.update_position()
    
    @property
    def center(self) -> tuple[float, float]:
        return self.x, self.y