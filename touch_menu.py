import pygame

pygame.font.init()

TEXT_SIZE = 30
FONT = pygame.font.Font("data/Open_Sans/static/OpenSans-Bold.ttf", size=TEXT_SIZE)

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

class Slider:
    def __init__(self, name, min, max, callback):
        self.name = name
        self.min = min
        self.max = max
        self.callback = callback
        self.rendered_name = FONT.render(self.name, True, WHITE, BLACK)
        self.value = (min + max) * 0.5
        self.rendered_value = FONT.render(str(self.value), True, WHITE, BLACK)
        self.rendered_min = FONT.render(str(self.min), True, WHITE, BLACK)
        self.rendered_max = FONT.render(str(self.max), True, WHITE, BLACK)
    
    def draw(self, surface):
        surface.blit(self.rendered_name, (
            surface.get_width() * 0.5 - self.rendered_name.get_width() * 0.5,
            surface.get_height() * 0.5 - self.rendered_name.get_height()
            ))
        
        surface.blit(self.rendered_value, (
            surface.get_width() * 0.5 - self.rendered_value.get_width() * 0.5,
            surface.get_height() * 0.5
        ))

        surface.blit(self.rendered_min, (
            50,
            surface.get_height() * 0.5
        ))

        surface.blit(self.rendered_max, (
            surface.get_width() - self.rendered_max.get_width() - 50,
            surface.get_height() * 0.5
        ))

    def handle_input(self):
        pass