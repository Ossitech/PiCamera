import pygame
import pygame_gui

class Gui:
    def __init__(self, screen_size: tuple[int, int]):
        self.screen_size = screen_size
        self.screen_width = screen_size[0]
        self.screen_height = screen_size[1]
        self.exposure_time_changed_callback = None

    def setup(self):
        self.ui_manager = pygame_gui.UIManager(self.screen_size)
        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (50, 40)),
            text='Menu',
            manager=self.ui_manager,
            command=self.toggle_menu
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((self.screen_width - 10 - 50, 10), (50, 40)),
            text='Exit',
            manager=self.ui_manager,
            command=self.exit_callback
        )
        self.menu_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((60, 60), (self.screen_width - 120, self.screen_height - 120)),
            manager=self.ui_manager,
            visible=False
        )

        self.exposure_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((100, 100), (600, 50)),
            manager=self.ui_manager,
            # container=self.menu_panel,
            start_value=0,
            value_range=(0, 100),
            click_increment=1,
        )

        self.exposure_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((100, 210), (200, 50)),
            manager=self.ui_manager,
            text=f"Auto Exposure"
        )
    
    def toggle_menu(self):
        if self.menu_panel.visible:
            # self.menu_panel.visible = False
            self.menu_panel.visible = False
            self.menu_button.set_text("Menu")
        else:
            self.menu_panel.visible = True
            self.menu_button.set_text("Close")
    
    def process_event(self, event):
        self.ui_manager.process_events(event)

        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.exposure_slider:
                if self.exposure_slider.current_value == 0:
                    self.exposure_label.set_text("Auto exposure")
                else:
                    self.exposure_label.set_text(f"Exposure time (us): {self.exposure_slider.current_value}")

                if self.exposure_time_changed_callback:
                    self.exposure_time_changed_callback(self.exposure_slider.current_value)

    def update(self, delta: float):
        self.ui_manager.update(delta)
    
    def draw(self, surface: pygame.Surface):
        self.ui_manager.draw_ui(surface)
    
    # callback must be a function that receives an int value,
    # which is the exposure time in us.
    def set_exposure_time_callback(self, callback):
        self.exposure_time_changed_callback = callback
    
    def set_exit_callback(self, callback):
        self.exit_callback = callback