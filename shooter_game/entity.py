import pygame

from pg_utils import ScreenEvents

from utils_pack.colors import ColorGradient, ColorPoint


class Entity(ScreenEvents):

    hp_gradient = ColorGradient(
        ColorPoint([255, 0, 0], 0),
        ColorPoint([255, 0, 0], 0.2),
        ColorPoint([255, 255, 0], 0.5),
        ColorPoint([0, 255, 0], 1)
    )

    def __init__(self, x: int, y: int, hp: int = 1, weapon: type = None):
        super().__init__()

        self.hp = hp
        self.max_hp = hp

        self._x = x
        self._y = y

        self.surf = pygame.Surface((20, 40))
        self.rect = self.surf.get_rect(center=(x, y))

        
        self.weapon = weapon(self) if isinstance(weapon, type) else weapon

    def draw(self) -> None:
        self.screen.blit(self.surf, self.rect)
        self.draw_hp()

    def draw_hp(self) -> None:
        background_surf = pygame.Surface((40, 5))
        background_rect = background_surf.get_rect(midbottom=(self.rect.centerx, self.rect.top - 5))
        hp_ratio = self.hp / self.max_hp
        ratio_width = int((background_surf.get_width() - 2) * hp_ratio)

        background_surf.fill("white")

        color = self.hp_gradient(hp_ratio)

        ratio_surf = pygame.Surface((ratio_width, background_surf.get_height() - 2))
        ratio_surf.fill(color)

        background_surf.blit(ratio_surf, (1, 1))

        self.screen.blit(background_surf, background_rect)

    def get_hit(self, damage: int = 1) -> None:
        self.hp = max(self.hp - damage, 0)

    def fire(self, direction: tuple[float, float]) -> None:
        if self.weapon is not None and direction != (0, 0):
            self.weapon.fire(direction)

    def update(self) -> None:
        if self.weapon is not None:
            self.weapon.update()
        
    def set_weapon(self, weapon) -> None:
        self.weapon = weapon

    @property
    def x(self) -> int:
        return self._x
    
    @x.setter
    def x(self, new_val: int) -> None:
        self._x = new_val
        self.rect.centerx = new_val

    @property
    def y(self) -> int:
        return self._y
    
    @y.setter
    def y(self, new_val: int) -> None:
        self._y = new_val
        self.rect.centery = new_val

    @property
    def center(self) -> tuple[int, int]:
        return self._x, self._y

    
    