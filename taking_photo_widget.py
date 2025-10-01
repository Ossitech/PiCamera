import pygame
import pygame_gui
from hidable_panel import HidablePanel

class TakingPhotoWidget(HidablePanel):
    def __init__(self, ui_manager: pygame_gui.UIManager):
        super().__init__(((300, 200), (200, 100)), ui_manager)

        self.label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((10, 10), (180, 80)),
            manager=ui_manager,
            container=self.panel,
            text="Taking Photo..."
        )