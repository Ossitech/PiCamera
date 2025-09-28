import pygame
import pygame_gui
from hidable_panel import HidablePanel
import numpy as np

class ExposureSettings(HidablePanel):
    def __init__(self, ui_manager: pygame_gui.UIManager, exposure_changed_callback):
        super().__init__(((100, 250), (600, 180)), ui_manager)

        self.callback = exposure_changed_callback

        self.exposure_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((50, 80), (500, 50)),
            manager=self.ui_manager,
            container=self.panel,
            start_value=0,
            value_range=(0.0, 100.0),
            click_increment=0.01,
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
            self.exposure_label.set_text(f"Exposure time (us): {log_scale(self.exposure_slider.current_value)}")

        if self.callback:
            self.callback(self.exposure_slider.current_value)
    
def log_scale(x: float, in_min: float = 0, in_max: float = 100, out_max: float = 200_000_000) -> float:
    if not (in_min <= x <= in_max):
        raise ValueError(f"Wert {x} liegt außerhalb des Eingabebereichs [{in_min}, {in_max}]")

    # Damit log(0) nicht auftritt, verschieben wir den Wertebereich leicht
    # z.B. Eingabe 0 → log(1), Eingabe 100 → log(B)
    shift = 1
    base = (in_max + shift)

    # normierte logarithmische Skala von 0..1
    norm = np.log(x + shift) / np.log(base)

    # auf den Zielbereich skalieren
    return norm * out_max