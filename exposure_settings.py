import pygame
import pygame_gui
from hidable_panel import HidablePanel

class ExposureSettings(HidablePanel):
    def __init__(self, ui_manager: pygame_gui.UIManager, exposure_changed_callback):
        super().__init__(((100, 250), (600, 180)), ui_manager)

        self.callback = exposure_changed_callback

        self.exposure_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((50, 80), (500, 50)),
            manager=self.ui_manager,
            container=self.panel,
            start_value=0,
            value_range=(0, 100),
            click_increment=1,
        )

        self.exposure_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((150, 15), (300, 50)),
            manager=self.ui_manager,
            container=self.panel,
            text=f"Auto Exposure",
            object_id=pygame_gui.core.ObjectID(class_id="@title_label")
        )
    
    def process_event(self, event):
        if event.type != pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            return
        
        if event.ui_element != self.exposure_slider:
            return
        
        if self.exposure_slider.current_value == 0:
            self.exposure_label.set_text("Auto exposure")
        else:
            self.exposure_label.set_text(f"Exposure time (us): {self.exposure_slider.current_value}")

        if self.callback:
            self.callback(self.exposure_slider.current_value)