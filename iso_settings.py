import pygame
import pygame_gui
from hidable_panel import HidablePanel

class ISOSettings(HidablePanel):
    def __init__(
            self,
            ui_manager: pygame_gui.UIManager,
            iso_changed_callback,
            auto_iso_toggle_callback,
            back_callback
        ):
        super().__init__(((100, 200), (600, 220)), ui_manager)

        self.iso_changed_callback = iso_changed_callback
        self.auto_iso_toggle_callback = auto_iso_toggle_callback

        self.back_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (100, 30)),
            manager=ui_manager,
            container=self.panel,
            text="< Back",
            command=back_callback
        )

        self.iso_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((100, 40), (400, 50)),
            manager=self.ui_manager,
            container=self.panel,
            text="Auto ISO",
            object_id=pygame_gui.core.ObjectID(class_id="@title_label")
        )

        self.iso_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((50, 90), (500, 50)),
            manager=self.ui_manager,
            container=self.panel,
            start_value=100,
            value_range=(100, 800),
            click_increment=50,
        )
        self.iso_slider.disable()

        self.auto_iso_checkbox = pygame_gui.elements.UICheckBox(
            relative_rect=pygame.Rect((480, 10), (30, 30)),
            manager=ui_manager,
            container=self.panel,
            initial_state=True,
            text="Auto Gain Control",
        )

    def process_event(self, event):
        if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED:
            if event.ui_element == self.iso_slider:
                iso_value = int(round(self.iso_slider.current_value))
                self.update_iso_label(iso_value)
                if self.iso_changed_callback:
                    self.iso_changed_callback(self.iso_to_gain(iso_value))

        elif event.type == pygame_gui.UI_CHECK_BOX_CHECKED:
            if event.ui_element == self.auto_iso_checkbox:
                self.iso_slider.disable()
                self.iso_label.set_text("Auto ISO")
                if self.auto_iso_toggle_callback:
                    self.auto_iso_toggle_callback(True)

        elif event.type == pygame_gui.UI_CHECK_BOX_UNCHECKED:
            if event.ui_element == self.auto_iso_checkbox:
                self.iso_slider.enable()
                iso_value = int(round(self.iso_slider.current_value))
                self.update_iso_label(iso_value)
                if self.auto_iso_toggle_callback:
                    self.auto_iso_toggle_callback(False)
                if self.iso_changed_callback:
                    self.iso_changed_callback(self.iso_to_gain(iso_value))

    def update_iso_label(self, iso_value: int):
        self.iso_label.set_text(f"ISO {iso_value}")

    @staticmethod
    def iso_to_gain(iso_value: int) -> float:
        return max(iso_value, 100) / 100.0
