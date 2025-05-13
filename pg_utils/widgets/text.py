import pygame

from .widget import Widget

from typing import Union


class Text(Widget):

    instances: "Text" = []

    def __init__(self,
                    text: str,
                    size: tuple = None,
                    font: str = "Arial",
                    fontsize: int = 20,
                    color: Union[str, tuple] = "white",
                    **position: tuple
                    ):
        super().__init__()
        

        self.surf = None
        self.rect = None
        self._font = font
        self._fontsize = fontsize
        self._size = size
        self._color = color
        self._text = None
        self._position = position
        

        self.text = text

        self.generate_text()

    def generate_text(self) -> None:
        font = pygame.font.SysFont(self._font, self._size)

        self.surf = font.render(self._text, True, self._color)
        self.rect = self.surf.get_rect(**self._position)
        
    @property
    def font(self) -> str:
        return self._font
    
    @font.setter
    def font(self, new_font: str) -> None:
        self._font = new_font
        self.generate_text()

    @property
    def size(self) -> str:
        return self._size
    
    @size.setter
    def size(self, new_size: int) -> None:
        self._size = new_size
        self.generate_text()

    @property
    def color(self) -> Union[str, tuple]:
        return self._color
    
    @color.setter
    def font(self, new_color: Union[str, tuple]) -> None:
        self._color = new_color
        self.generate_text()

    @property
    def font(self) -> str:
        return self._font
    
    @font.setter
    def font(self, new_font: str) -> None:
        self._font = new_font
        self.generate_text()

    @property
    def text(self) -> str:
        return self._text
    
    @text.setter
    def text(self, new_text: str) -> None:
        self._text = str(new_text)
        self.generate_text()
