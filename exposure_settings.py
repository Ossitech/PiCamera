import pygame
import pygame_gui
from hidable_panel import HidablePanel
import numpy as np

class ExposureSettings(HidablePanel):
    def __init__(
            self,
            ui_manager: pygame_gui.UIManager,
            exposure_changed_callback,
            back_callback
        ):
        super().__init__(((100, 250), (600, 180)), ui_manager)

        self.callback = exposure_changed_callback

        self.exposure_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((50, 80), (500, 50)),
            manager=self.ui_manager,
            container=self.panel,
            start_value=0,
            value_range=(0.0, 1.0),
            click_increment=0.01,
        )

        self.exposure_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((100, 15), (400, 50)),
            manager=self.ui_manager,
            container=self.panel,
            text=f"Auto Exposure",
            object_id=pygame_gui.core.ObjectID(class_id="@title_label")
        )

        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (100, 30)),
            manager=ui_manager,
            container=self.panel,
            text="< Back",
            command=back_callback
        )
    
    def process_event(self, event):
        if event.type != pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            return
        
        if event.ui_element != self.exposure_slider:
            return
        
        if self.exposure_slider.current_value == 0:
            self.exposure_label.set_text("Auto Exposure")
        else:
            scaled_value = exposure_scale(self.exposure_slider.current_value)
            formated_value = format_microseconds(scaled_value)
            self.exposure_label.set_text(f"Exposure Time: {formated_value}")

        if self.callback:
            self.callback(int(self.exposure_slider.current_value))
    
def exposure_scale(x: float):
    return 200_000_000 * (x ** 7.388)

def format_microseconds(value: int) -> str:
    if value >= 60_000_000:
        minutes = int(value / 60_000_000)
        seconds = int(((value / 60_000_000) - minutes) * 60)
        return f"{minutes}:{seconds:02d} Minutes"
    elif value >= 1_000_000:
        seconds = value / 1_000_000
        return f"{seconds:.2f} Seconds"
    elif value >= 1_000:
        millis = value / 1_000
        return f"{millis:.0f} Milliseconds"
    else:
        return f"{value:.0f} Microseconds"