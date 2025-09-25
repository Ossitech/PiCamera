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

        self.build_ui()

    def run(self):
        self.running = True
        self.camera.start_preview()
        while self.running:
            self.handle_events()
            self.screen.fill((0, 0, 0))
            if self.camera.preview_frame_available:
                self.current_preview_frame = self.camera.get_pygame_preview_frame()
            if self.current_preview_frame == None:
                self.screen.blit(self.no_signal_image, (0, 0))
            else:
                self.screen.blit(self.current_preview_frame, (0, 0))
            self.ui_manager.draw_ui(self.screen)
            pygame.display.update()
            self.delta = self.clock.tick(FPS) * 0.001

    def handle_events(self):
        time_delta = self.clock.tick(FPS)/1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

            self.ui_manager.process_events(event)
            self.ui_manager.update(time_delta)

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
        exit()

    def calc_centered_rect_pos_in_rect(outer_size: tuple, inner_size: tuple):
        return (int(outer_size[0] / 2 - inner_size[0] / 2), int(outer_size[1] / 2 - inner_size[1] / 2))
    
    def toggle_menu(self):
        if self.menu_panel.visible:
            self.menu_panel.visible = False
            self.menu_button.set_text("Menu")
        else:
            self.menu_panel.visible = True
            self.menu_button.set_text("Close")

    def build_ui(self):
        # pygame_gui
        self.ui_manager = pygame_gui.UIManager(SCREEN_SIZE)
        self.menu_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((10, 10), (50, 40)),
            text='Menu',
            manager=self.ui_manager,
            command=self.toggle_menu
        )
        self.exit_button = pygame_gui.elements.UIButton(
            relative_rect=pygame.Rect((SCREEN_SIZE[0] - 10 - 50, 10), (50, 40)),
            text='Exit',
            manager=self.ui_manager,
            command=self.quit
        )
        self.menu_visible = False
        self.menu_panel = pygame_gui.elements.UIPanel(
            relative_rect=pygame.Rect((60, 60), (SCREEN_SIZE[0] - 120, SCREEN_SIZE[1] - 120)),
            # starting_layer_height=1,
            manager=self.ui_manager,
            visible=False
        )


if __name__ == "__main__":
    app = CameraApp()
    app.run()