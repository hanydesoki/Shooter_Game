import random

import pygame

from pg_utils import ScreenEvents

from .player import Player
from .ennemy import Ennemy, Boss
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
                    if ennemy.rect.collidepoint(bullet.center) and ennemy not in bullet.hitted_targets:
                        ennemy.get_hit(bullet.damage)
                        bullet.hp = max(bullet.hp - 1, 0)
                        bullet.hitted_targets.append(ennemy)
            # ennemy bullets
            elif isinstance(bullet.owner, Ennemy):
                if self.player.rect.collidepoint(bullet.center) and self.player not in bullet.hitted_targets:
                    self.player.get_hit(bullet.damage)
                    bullet.hp = max(bullet.hp - 1, 0)
                    bullet.hitted_targets.append(self.player)


            if bullet.hp <= 0:
                bullet.remove_instance()
            


    def manage_ennemies(self) -> None:
        # Spawn ennemy
        if random.random() < 0.01 and len(self.ennemies) < 5:
            x, y = self.generate_random_outbound_spawn_coord()

            weapon = None

            ennemy_type = Ennemy

            if random.random() < 0.1:
                weapon = random.choices(list(self.weapons.keys()), list(self.weapons.values()))[0]

            # Randomly can be a boss
            if random.random() < 0.1:
                ennemy_type = Boss

            ennemy = ennemy_type(
                self.player,
                x,
                y,
                hp=ennemy_type.default_hp,
                weapon=weapon
            )

            self.ennemies.append(ennemy)


        bosses: list[Boss] = []

        for ennemy in self.ennemies[:]:

            if ennemy.rect.colliderect(self.player.rect):
                self.ennemies.remove(ennemy)
                self.player.get_hit(1)
                continue

            if ennemy.hp <= 0:
                self.ennemies.remove(ennemy)
                continue

            if isinstance(ennemy, Boss):
                bosses.append(ennemy)

            ennemy.update()
            ennemy.draw()

        # Draw boss lifebar
        for i, boss in enumerate(bosses):
            background_surf = pygame.Surface((int(self.screen_width * 0.8), 5))
            background_rect = background_surf.get_rect(
                midbottom=(
                    self.screen_center[0], 
                    self.screen_height - 10 - i *(background_surf.get_height() + 10)
                )
            )
            hp_ratio = boss.hp / boss.max_hp
            ratio_width = int((background_surf.get_width() - 2) * hp_ratio)

            background_surf.fill("white")

            color = Boss.hp_gradient(hp_ratio)

            ratio_surf = pygame.Surface((ratio_width, background_surf.get_height() - 2))
            ratio_surf.fill(color)

            background_surf.blit(ratio_surf, (1, 1))
            self.screen.blit(background_surf, background_rect)


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

        text_rect = text_surf.get_rect(topleft=(20, 20))

        self.screen.blit(text_surf, text_rect)


    def generate_random_outbound_spawn_coord(self) -> tuple[int, int]:
        x = random.randint(0, 100) + (-100 if random.random() < 0.5 else self.screen_width + 100)
        y = random.randint(0, 100) + (-100 if random.random() < 0.5 else self.screen_height + 100)

        return x, y
    
    # def get_bosses(self) -> list[Boss]:
    #     return [e for e in self.ennemies if isinstance(e, Boss)]

    def update(self) -> None:
        self.draw_background()
        self.player.update()
        
        self.player.draw()
        self.manage_bullet()
        self.manage_ennemies()
        self.manage_pickups()

        self.draw_ui()