import pygame
import pygame_gui
from hidable_panel import HidablePanel

class WhiteBalanceSettings(HidablePanel):
    def __init__(
            self,
            ui_manager: pygame_gui.UIManager,
            back_callback,
            wb_changed_callback
        ):
        super().__init__(((100, 150), (600, 280)), ui_manager)

        self.callback = wb_changed_callback

        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (100, 30)),
            manager=ui_manager,
            container=self.panel,
            text="< Back",
            command=back_callback
        )

        self.red_gain_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((100, 30), (400, 50)),
            manager=self.ui_manager,
            container=self.panel,
            text=f"Red Gain: 1.0",
            object_id=pygame_gui.core.ObjectID(class_id="@title_label")
        )

        self.red_gain_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((50, 70), (500, 50)),
            manager=self.ui_manager,
            container=self.panel,
            start_value=1.0,
            value_range=(0.0, 4.0),
            click_increment=0.01,
        )

        self.blue_gain_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((100, 140), (400, 50)),
            manager=self.ui_manager,
            container=self.panel,
            text=f"Blue Gain: 1.0",
            object_id=pygame_gui.core.ObjectID(class_id="@title_label")
        )

        self.blue_gain_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((50, 180), (500, 50)),
            manager=self.ui_manager,
            container=self.panel,
            start_value=1.0,
            value_range=(0.0, 4.0),
            click_increment=0.01,
        )
    
    def process_event(self, event):
        if event.type != pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            return
        
        if event.ui_element == self.red_gain_slider:
            self.update_red_label(self.red_gain_slider.current_value)
        
        if event.ui_element == self.blue_gain_slider:
            self.update_blue_label(self.blue_gain_slider.current_value)
        
        if self.callback:
            self.callback(self.red_gain_slider.current_value, self.blue_gain_slider.current_value)
    
    def update_red_label(self, value):
        self.red_gain_label.set_text(f"Red Gain: {value:.2f}")
    
    def update_blue_label(self, value):
        self.blue_gain_label.set_text(f"Blue Gain: {value:.2f}")