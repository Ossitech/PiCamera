import pygame
import os
import random
import time
import numpy as np
import camera
import hardware_controls
from gui import Gui

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

        self.gui = Gui(SCREEN_SIZE)
        self.gui.set_exposure_time_callback(self._on_exposure_changed)
        self.gui.set_exit_callback(self.quit)
        self.gui.set_wb_callback(self._on_white_balance_changed)
        self.gui.setup()

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

            self.gui.draw(self.screen)

            pygame.display.update()

            self.delta = self.clock.tick(FPS) * 0.001

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_ESCAPE:
                    self.quit()

            self.gui.process_event(event)
        self.gui.update(self.delta)

        for button, action in self.camera_controls.get_events():
            print(button, action)
            if button == hardware_controls.EVENT_BUTTON and action == hardware_controls.EVENT_DOWN:
                self.take_photo()
    
    def take_photo(self):
        self.camera.take_photo()
    
    def quit(self):
        self.camera.stop_preview()
        self.camera.quit()
        self.camera_controls.quit()
        pygame.quit()
        exit()
    
    def _on_exposure_changed(self, exposure_time_us: int):
        if exposure_time_us == 0:
            self.camera.set_auto_exposure()
            return
        
        self.camera.set_exposure_time(exposure_time_us)
    
    def _on_white_balance_changed(self, red_gain, blue_gain):
        self.camera.set_color_gains(red_gain, blue_gain)


if __name__ == "__main__":
    app = CameraApp()
    app.run()