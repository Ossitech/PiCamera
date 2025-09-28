import pygame
import pygame_gui

from exposure_settings import ExposureSettings

HIDE_OFFSET = 1000

class Gui:
    def __init__(self, screen_size: tuple[int, int]):
        self.screen_size = screen_size
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
        self.exposure_time_changed_callback = None
        self.exit_callback = None
        self.setup_finished = False

    def setup(self):
        self.ui_manager = pygame_gui.UIManager(self.screen_size, "data/theme.json")
        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (50, 40)),
            text='Menu',
            manager=self.ui_manager,
            command=self.toggle_menu
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_width - 10 - 50, 10), (30, 38)),
            text='X',
            manager=self.ui_manager,
            command=self.exit_callback
        )

        self.exposure_settings = ExposureSettings(
            self.ui_manager,
            self.exposure_time_changed_callback
        )
        self.exposure_settings.hide()

        self.setup_finished = True
    
    def toggle_menu(self):
        if self.exposure_settings.is_visible():
            self.exposure_settings.hide()
            self.menu_button.set_text("Menu")
        else:
            self.exposure_settings.show()
            self.menu_button.set_text("Close")
    
    def process_event(self, event):
        self.ui_manager.process_events(event)
        self.exposure_settings.process_event(event)

    def update(self, delta: float):
        self.ui_manager.update(delta)
    
    def draw(self, surface: pygame.Surface):
        self.ui_manager.draw_ui(surface)
    
    # callback must be a function that receives an int value,
    # which is the exposure time in us.
    def set_exposure_time_callback(self, callback):
        if self.setup_finished:
            raise Exception("Can't set callback after setup was called!")
        
        self.exposure_time_changed_callback = callback
    
    def set_exit_callback(self, callback):
        if self.setup_finished:
            raise Exception("Can't set callback after setup was called!")
        
        self.exit_callback = callback