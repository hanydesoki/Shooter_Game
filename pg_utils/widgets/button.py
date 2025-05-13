import pygame

from .widget import Widget

from typing import Union


class Button(Widget):

    instances: list["Button"] = []
    
    def __init__(self, text: str,
                    size: tuple = None,
                    font: str = "Arial",
                    fontsize: int = 20,
                    text_color: Union[str, tuple] = "white",
                    top_color: Union[str, tuple] = "blue",
                    bottom_color: Union[str, tuple] = "red",
                    depth: int = 5,
                    **position: tuple
                    ) -> None:
        
        super().__init__()
        
        self.text = text
        self.size = size
        self.depth = depth

        self.text_surf = pygame.font.SysFont(font, fontsize).render(text, True, text_color)

        self.bottom_surf = pygame.Surface(self.text_surf.get_size() if size is None else size)
        self.bottom_surf.fill(bottom_color)
        self.top_surf = pygame.Surface(self.bottom_surf.get_size())
        self.top_surf.fill(top_color)
        self.rect = self.bottom_surf.get_rect(**position)

        self.bottom_rect = self.rect

        self.top_rect = self.top_surf.get_rect(midbottom=(self.bottom_rect.centerx,
                                                           self.bottom_rect.bottom - self.depth))
        
        self.text_rect = self.text_surf.get_rect(center=self.top_rect.center)

        self._clicks = [False, False] 
        self.pressed = False

        self.add_instance()

    def draw(self) -> None:
        self.screen.blit(self.bottom_surf, self.bottom_rect)
        self.screen.blit(self.top_surf, self.top_rect)
        self.screen.blit(self.text_surf, self.text_rect)


    def manage_click(self) -> None:
        mouse_pos = pygame.mouse.get_pos()

        self.top_rect.midbottom = (self.bottom_rect.centerx, self.bottom_rect.bottom - self.depth)

        self.pressed = pygame.mouse.get_pressed()[0] and self.bottom_rect.collidepoint(mouse_pos)

        if self.pressed:
            self.top_rect.midbottom = self.bottom_rect.midbottom

        self.text_rect.center = self.top_rect.center
        self._clicks.append(self.pressed)
        self._clicks.pop(0)

    @property
    def released(self) -> bool:
        return self._clicks == [True, False] and not pygame.mouse.get_pressed()[0]
    
    @property
    def clicked(self) -> bool:
        return self.mouse_clicked()

    def update(self) -> None:
        self.manage_click()
        self.draw()

    @classmethod
    def update_all(cls) -> None:
        for button in cls.instances:
            button.update()
