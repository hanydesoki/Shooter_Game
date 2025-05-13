import random

import pygame

from pg_utils import ScreenEvents

from .player import Player
from .ennemy import Ennemy
from .bullet import Bullet

from .weapon import *

from .pickup import PickUp, WeaponPickups

class Layout(ScreenEvents):

    weapons = {
        Pistol: 3,
        Magnum: 2,
        AssaultRifle: 1
    }

    def __init__(self):
        super().__init__()

        self.player: Player = Player(
            *self.screen_center,
            10,
            Pistol
        )

        self.ennemies: list[Ennemy] = []
        self.pickups: list[PickUp] = []

        self.font = pygame.font.SysFont("Arial", 20)

    def draw_background(self) -> None:
        pygame.draw.rect(
            self.screen,
            (50, 50, 50),
            self.screen.get_rect()
        )

    def manage_bullet(self) -> None:
        for bullet in Bullet.all_bullets[:]:
            
            bullet.update()
            bullet.draw()

            if not bullet.is_inbound():
                bullet.remove_instance()
                continue
            
            # player bullets
            if bullet.owner is self.player:
                for ennemy in self.ennemies[:]:
                    if ennemy.rect.collidepoint(bullet.center):
                        ennemy.get_hit(bullet.damage)
                        bullet.hp = max(bullet.hp - 1, 0)
            # ennemy bullets
            elif isinstance(bullet.owner, Ennemy):
                if self.player.rect.collidepoint(bullet.center):
                    self.player.get_hit(bullet.damage)


            if bullet.hp <= 0:
                bullet.remove_instance()
            


    def manage_ennemies(self) -> None:
        # Spawn ennemy
        if random.random() < 0.01 and len(self.ennemies) < 5:
            x = random.randint(0, 100) + (-100 if random.random() < 0.5 else self.screen_width + 100)
            y = random.randint(0, 100) + (-100 if random.random() < 0.5 else self.screen_height + 100)

            weapon = None

            if random.random() < 0.1:
                weapon = random.choices(list(self.weapons.keys()), list(self.weapons.values()))[0]

            ennemy = Ennemy(
                self.player,
                x,
                y,
                pv=2,
                weapon=weapon
            )

            self.ennemies.append(ennemy)

        for ennemy in self.ennemies[:]:

            if ennemy.rect.colliderect(self.player.rect):
                self.ennemies.remove(ennemy)
                self.player.get_hit(1)
                continue

            if ennemy.hp <= 0:
                self.ennemies.remove(ennemy)
                continue

            ennemy.update()
            ennemy.draw()
    
    def manage_pickups(self) -> None:

        if random.random() < 0.001 and len(self.pickups) < 2:
            x = random.randint(0, self.screen_width)
            y = random.randint(0, self.screen_height)

            random_weapon = random.choices(list(self.weapons.keys()), list(self.weapons.values()))[0]

            pickup = WeaponPickups(
                x,
                y,
                random_weapon(self.player)
            )

            self.pickups.append(pickup)

        for pickup in self.pickups[:]:
            if pickup.rect.colliderect(self.player.rect):
                self.pickups.remove(pickup)
                if isinstance(pickup, WeaponPickups):
                    self.player.set_weapon(pickup.weapon)
                continue

            pickup.draw()

    def draw_ui(self) -> None:
        if self.player.weapon is None:
            return
        
        weapon: Weapon = self.player.weapon
        text = f"{weapon.name}: {weapon.bullets} / {weapon.mag_size}"

        text_surf = self.font.render(text, True, "white" if weapon.bullets else "red")

        text_rect = text_surf.get_rect(bottomleft=(20, self.screen_height - 20))

        self.screen.blit(text_surf, text_rect)




    def update(self) -> None:
        self.draw_background()
        self.player.update()
        
        self.player.draw()
        self.manage_bullet()
        self.manage_ennemies()
        self.manage_pickups()

        self.draw_ui()