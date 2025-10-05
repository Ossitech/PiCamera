import pygame
import pygame_gui
import time
from hidable_panel import HidablePanel

class ResultView(HidablePanel):
    def __init__(self, ui_manager, screen_size):
        super().__init__(((0, screen_size[1] - 30), (screen_size[0], 30)), ui_manager)

        self.progress_bar = pygame_gui.elements.UIProgressBar(
            manager=ui_manager,
            container=self.panel,
            relative_rect=pygame.Rect((0, 0), (screen_size[0], 30)),
        )

        self.result_image = None
        self.timestamp = 0
    
    def load_image(self, filePath):
        self.result_image = pygame.image.load(filePath).convert()
        self.result_image = pygame.transform.scale(self.result_image, self.screen_size)
    
    def draw(self, surface: pygame.Surface):
        if self.result_image == None:
            return
        
        surface.blit(self.result_image)
        
        now = time.time()
        seconds = now - self.timestamp

        self.progress_bar.set_current_progress(100.0 - seconds * 20.0)

        if seconds > 5:
            self.reset()
    
    def show_result(self, filePath):
        self.load_image(filePath)
        self.show()
        self.timestamp = time.time()
    
    def reset(self):
        self.result_image = None
        self.hide()