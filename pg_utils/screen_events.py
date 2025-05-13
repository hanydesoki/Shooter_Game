import pygame


class ScreenEvents:

    all_events: list[pygame.event.Event] = []

    def __init__(self):
        self.screen = pygame.display.get_surface()
        self.screen_width = self.screen.get_width()
        self.screen_height = self.screen.get_height()
        self.screen_center = (self.screen_width // 2, self.screen_height // 2)

    @classmethod
    def update_events(cls, events: list[pygame.event.Event]) -> None:
        cls.all_events = events

    def key_pressed(self, *keys: int) -> bool:
        for event in self.all_events:
            if event.type == pygame.KEYDOWN:
                if event.key in keys:
                    return True
                
        return False
    
    def mouse_clicked(self, index: int = 0) -> bool:
        for event in self.all_events:
            if event.type == pygame.MOUSEBUTTONDOWN:
                return pygame.mouse.get_pressed()[index]
            
        return False
