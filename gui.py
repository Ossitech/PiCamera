import pygame
import pygame_gui

from main_menu import MainMenu

HIDE_OFFSET = 1000

class Gui:
    def __init__(self, screen_size: tuple[int, int]):
        self.screen_size = screen_size
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
        self.exposure_time_changed_callback = None
        self.exit_callback = None
        self.wb_callback = None
        self.awb_toggle_callback = None
        self.iso_changed_callback = None
        self.auto_iso_toggle_callback = None
        self.setup_finished = False

    def setup(self):
        self.ui_manager = pygame_gui.UIManager(self.screen_size, "data/theme.json")
        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (50, 40)),
            text='Menu',
            manager=self.ui_manager,
            command=self.show_menu
        )

        self.main_menu = MainMenu(
            self.ui_manager,
            self.exposure_time_changed_callback,
            self.iso_changed_callback,
            self.auto_iso_toggle_callback,
            self.exit_callback,
            self.on_menu_closed,
            self.wb_callback,
            self.awb_toggle_callback
        )
        self.main_menu.hide()

        self.setup_finished = True
    
    def show_menu(self):
        self.menu_button.hide()
        self.main_menu.show()
    
    def process_event(self, event):
        self.ui_manager.process_events(event)
        self.main_menu.process_event(event)

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
    
    def on_menu_closed(self):
        self.menu_button.visible = True
    
    def set_wb_callbacks(self, gains_changed_callback, awb_toggle_callback):
        if self.setup_finished:
            raise Exception("Can't set callback after setup was called!")
        
        self.wb_callback = gains_changed_callback
        self.awb_toggle_callback = awb_toggle_callback

    def set_iso_callbacks(self, iso_changed_callback, auto_iso_toggle_callback):
        if self.setup_finished:
            raise Exception("Can't set callback after setup was called!")

        self.iso_changed_callback = iso_changed_callback
        self.auto_iso_toggle_callback = auto_iso_toggle_callback
