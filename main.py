import pygame
import os
import random
import time
import camera
import hardware_controls
import pygame_gui
import numpy as np

pygame.init()


SCREEN_SIZE = (800, 480)
CROP_SIZE = (150, 150)
FPS = 144

class CameraApp:
    def __init__(self):
        self.screen = pygame.display.set_mode(SCREEN_SIZE, pygame.FULLSCREEN)
        self.clock = pygame.time.Clock()
        self.delta = self.clock.tick(FPS)
        self.running = False
        self.no_signal_image = pygame.image.load("data/no_signal.png")
        self.camera = camera.Camera(SCREEN_SIZE, FPS)
        self.current_preview_frame = None
        self.camera_controls = hardware_controls.CameraControls()

        # pygame_gui
        self.ui_manager = pygame_gui.UIManager(SCREEN_SIZE)
        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (50, 40)),
            text='≡',
            manager=self.ui_manager
        )
        self.menu_visible = False
        self.menu_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((0, 0), SCREEN_SIZE),
            # starting_layer_height=1,
            manager=self.ui_manager,
            visible=False
        )
        self.menu_panel.background_colour = (0, 0, 0, 128)  # halbtransparent
        self.auto_exposure_checkbox = pygame_gui.elements.UISelectionList(
            relative_rect=pygame.Rect((SCREEN_SIZE[0]//2-100, 100, 200, 50)),
            item_list=["Automatische Belichtung"],
            manager=self.ui_manager,
            container=self.menu_panel
        )
        self.exposure_slider = pygame_gui.elements.UIHorizontalSlider(
            relative_rect=pygame.Rect((SCREEN_SIZE[0]//2-150, 180, 300, 40)),
            start_value=1000,
            value_range=(100, 60000000),
            manager=self.ui_manager,
            container=self.menu_panel
        )
        self.exposure_label = pygame_gui.elements.UILabel(
            relative_rect=pygame.Rect((SCREEN_SIZE[0]//2+160, 180, 120, 40)),
            text="1 ms",
            manager=self.ui_manager,
            container=self.menu_panel
        )
        self.exposure_slider.hide()
        self.exposure_label.hide()
        self.last_slider_value = 1000
        self.slider_min = 100
        self.slider_max = 60000000

    def run(self):
        self.running = True
        self.camera.start_preview()
        while self.running:
            time_delta = self.clock.tick(FPS)/1000.0
            self.handle_events()
            self.screen.fill((0, 0, 0))
            if self.camera.preview_frame_available:
                self.current_preview_frame = self.camera.get_pygame_preview_frame()
            if self.current_preview_frame == None:
                self.screen.blit(self.no_signal_image, (0, 0))
            else:
                self.screen.blit(self.current_preview_frame, (0, 0))
            self.ui_manager.update(time_delta)
            self.ui_manager.draw_ui(self.screen)
            pygame.display.update()
            self.delta = self.clock.tick(FPS) * 0.001

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.USEREVENT:
                if event.user_type == pygame_gui.UI_BUTTON_PRESSED and event.ui_element == self.menu_button:
                    self.menu_visible = not self.menu_visible
                    self.menu_panel.show() if self.menu_visible else self.menu_panel.hide()
                if event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION and event.ui_element == self.auto_exposure_checkbox:
                    self.camera.set_auto_exposure()
                    self.exposure_slider.hide()
                    self.exposure_label.hide()
                if event.user_type == pygame_gui.UI_SELECTION_LIST_DROPPED_SELECTION and event.ui_element == self.auto_exposure_checkbox:
                    self.exposure_slider.show()
                    self.exposure_label.show()
            if event.type == pygame_gui.UI_HORIZONTAL_SLIDER_MOVED and event.ui_element == self.exposure_slider:
                # Logarithmische Skalierung
                slider_value = self.exposure_slider.get_current_value()
                # Umwandlung in logarithmische Skala
                min_log = np.log10(self.slider_min)
                max_log = np.log10(self.slider_max)
                log_value = min_log + (max_log - min_log) * ((slider_value - self.slider_min) / (self.slider_max - self.slider_min))
                exposure_time = int(10 ** log_value)
                self.camera.set_exposure_time(exposure_time)
                self.exposure_label.set_text(f"{exposure_time/1000:.1f} ms" if exposure_time < 1000000 else f"{exposure_time/1000000:.2f} s")
        for button, action in self.camera_controls.get_events():
            print(button, action)
            if button == hardware_controls.EVENT_BUTTON and action == hardware_controls.EVENT_DOWN:
                self.take_photo()
    
    def take_photo(self):
        self.camera.take_photo()
    
    def quit(self):
        self.camera.stop_preview()
        self.camera_controls.quit()
        pygame.quit()

    def calc_centered_rect_pos_in_rect(outer_size: tuple, inner_size: tuple):
        return (int(outer_size[0] / 2 - inner_size[0] / 2), int(outer_size[1] / 2 - inner_size[1] / 2))


if __name__ == "__main__":
    app = CameraApp()
    app.run()