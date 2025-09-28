import pygame
import pygame_gui

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
        self.ui_manager = pygame_gui.UIManager(self.screen_size)
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
        self.menu_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((60, 60 - HIDE_OFFSET), (self.screen_width - 120, self.screen_height - 120)),
            manager=self.ui_manager,
        )

        self.exposure_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((100, 100), (480, 50)),
            manager=self.ui_manager,
            container=self.menu_panel,
            start_value=0,
            value_range=(0, 100),
            click_increment=1,
        )

        self.exposure_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((100, 210), (200, 50)),
            manager=self.ui_manager,
            container=self.menu_panel,
            text=f"Auto Exposure"
        )

        self.setup_finished = True
    
    def toggle_menu(self):
        rect = self.menu_panel.relative_rect
        # currently visible
        if rect.y > 0:
            # hide by moving out of view.
            self.menu_panel.set_relative_position((rect.x, rect.y - HIDE_OFFSET))
            self.menu_button.set_text("Menu")
        else:
            # show by moving back into view.
            self.menu_panel.set_relative_position((rect.x, rect.y + HIDE_OFFSET))
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
        if self.setup_finished:
            raise Exception("Can't set callback after setup was called!")
        
        self.exposure_time_changed_callback = callback
    
    def set_exit_callback(self, callback):
        if self.setup_finished:
            raise Exception("Can't set callback after setup was called!")
        
        self.exit_callback = callback