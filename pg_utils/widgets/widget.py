from ..screen_events import ScreenEvents
import pygame

from abc import ABC, abstractmethod


class Widget(ScreenEvents, ABC):

    widget_instances: list["Widget"] = []
    instances: list["Widget"] = []

    def __init__(self):
        super().__init__()

        self._position: dict[str, tuple[int, int]] = None
        self.rect: pygame.Rect = None
        self.add_widget_instance()

    def __post_init__(self) -> None:
        print("POST INIT")
        if not isinstance(self.rect):
            raise ValueError("rect attribute is not setted.")

    def add_widget_instance(self) -> None:
        self.widget_instances.append(self)

    def add_instance(self) -> None:
        self.instances.append(self)

    def set_position(self, **new_position: dict[str, tuple[int, int]]) -> None:
        self._position = new_position
        name, pos = next(iter(new_position.items()))
        exec(f"self.rect.{name} = {pos}")

    @abstractmethod
    def draw(self) -> None:
        pass

    @abstractmethod
    def update(self) -> None:
        pass

    @classmethod
    def update_all(cls) -> None:
        for button in cls.instances:
            button.update()