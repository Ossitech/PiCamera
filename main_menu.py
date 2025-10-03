import pygame
import pygame_gui
from hidable_panel import HidablePanel
from exposure_settings import ExposureSettings
from white_balance_settings import WhiteBalanceSettings
from iso_settings import ISOSettings

class MainMenu(HidablePanel):
    def __init__(
            self,
            ui_manager: pygame_gui.UIManager,
            exposure_changed_callback,
            iso_changed_callback,
            auto_iso_toggle_callback,
            exit_callback,
            menu_closed_callback,
            color_gains_changed_callback,
            awb_toggle_callback
        ):
        super().__init__(((160, 50), (480, 380)), ui_manager)

        self.menu_closed_callback = menu_closed_callback

        self.title = pygame_gui.elements.UILabel(
            manager=ui_manager,
            container=self.panel,
            text="Menu",
            relative_rect=pygame.Rect((180, 10), (100, 50)),
            object_id="@title_label"
        )

        self.back_button = pygame_gui.elements.UIButton(
            manager=ui_manager,
            container=self.panel,
            text="< Back",
            relative_rect=pygame.Rect((30, 30), (100, 50)),
            command=self.close_menu
        )

        self.white_balance_button = pygame_gui.elements.UIButton(
            manager=ui_manager,
            container=self.panel,
            text="White Balance",
            relative_rect=pygame.Rect((30, 130), (200, 50)),
            command=self.show_wb_settings
        )

        self.exposure_button = pygame_gui.elements.UIButton(
            manager=ui_manager,
            container=self.panel,
            text="Exposure Settings",
            relative_rect=pygame.Rect((30, 190), (200, 50)),
            command=self.show_exposure_settings
        )

        self.iso_button = pygame_gui.elements.UIButton(
            manager=ui_manager,
            container=self.panel,
            text="ISO Settings",
            relative_rect=pygame.Rect((30, 250), (200, 50)),
            command=self.show_iso_settings
        )

        self.exit_button = pygame_gui.elements.UIButton(
            manager=ui_manager,
            container=self.panel,
            text="Quit",
            relative_rect=pygame.Rect((350, 30), (100, 50)),
            command=exit_callback
        )

        self.wb_settings = WhiteBalanceSettings(
            self.ui_manager,
            self.show_main_menu,
            color_gains_changed_callback,
            awb_toggle_callback,
        )
        self.wb_settings.hide()

        self.exposure_settings = ExposureSettings(
            self.ui_manager,
            exposure_changed_callback,
            self.show_main_menu
        )
        self.exposure_settings.hide()

        self.iso_settings = ISOSettings(
            self.ui_manager,
            iso_changed_callback,
            auto_iso_toggle_callback,
            self.show_main_menu
        )
        self.iso_settings.hide()
    
    def process_event(self, event):
        self.exposure_settings.process_event(event)
        self.iso_settings.process_event(event)
        self.wb_settings.process_event(event)
    
    def show_main_menu(self):
        self.show()
        self.exposure_settings.hide()
        self.iso_settings.hide()
        self.wb_settings.hide()

    def show_exposure_settings(self):
        self.hide()
        self.exposure_settings.show()

    def show_iso_settings(self):
        self.hide()
        self.iso_settings.show()
    
    def close_menu(self):
        self.menu_closed_callback()
        self.hide()
    
    def show_wb_settings(self):
        self.hide()
        self.wb_settings.show()
