import pygame
import pygame_gui
from hidable_panel import HidablePanel

class WhiteBalanceSettings(HidablePanel):
    def __init__(
            self,
            ui_manager: pygame_gui.UIManager,
            back_callback,
            gain_changed_callback,
            awb_toggle_callback
        ):
        super().__init__(((100, 150), (600, 280)), ui_manager)

        self.gain_changed_callback = gain_changed_callback
        self.awb_changed_callback = awb_toggle_callback

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
            text=f"Red Gain: Auto",
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
        self.red_gain_slider.disable()

        self.blue_gain_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((100, 140), (400, 50)),
            manager=self.ui_manager,
            container=self.panel,
            text=f"Blue Gain: Auto",
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
        self.blue_gain_slider.disable()

        self.awb_checkbox = pygame_gui.elements.UICheckBox(
            relative_rect=pygame.Rect((420, 10), (30, 30)),
            manager=ui_manager,
            container=self.panel,
            initial_state=True,
            text="Auto White Balance",
        )
    
    def process_event(self, event):
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.red_gain_slider:
                self.update_red_label()
            
            if event.ui_element == self.blue_gain_slider:
                self.update_blue_label()
            
            if self.gain_changed_callback:
                self.gain_changed_callback(self.red_gain_slider.current_value, self.blue_gain_slider.current_value)
        
        elif event.type == pygame_gui.UI_CHECK_BOX_CHECKED:
            if event.ui_element == self.awb_checkbox:
                self.red_gain_slider.disable()
                self.blue_gain_slider.disable()
                self.red_gain_label.set_text("Red Gain: Auto")
                self.blue_gain_label.set_text("Blue Gain: Auto")
                self.awb_changed_callback(True)
        elif event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
            if event.ui_element == self.awb_checkbox:
                self.red_gain_slider.enable()
                self.blue_gain_slider.enable()
                self.update_red_label()
                self.update_blue_label()
                self.awb_changed_callback(False)
    
    def update_red_label(self):
        self.red_gain_label.set_text(f"Red Gain: {self.red_gain_slider.current_value:.2f}")
    
    def update_blue_label(self):
        self.blue_gain_label.set_text(f"Blue Gain: {self.blue_gain_slider.current_value:.2f}")