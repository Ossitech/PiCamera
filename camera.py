import pygame
import cv2
try:
    import picamera2
    onPi = True
except:
    onPi = False
import numpy as np
import time
import os
from threading import Thread

PHOTOS_PATH = "/home/ossitech/Synchronisierte Dateien/Pi Camera/photos"
VIDEOS_PATH = "/home/ossitech/Synchronisierte Dateien/Pi Camera/videos"

class Camera:
    def __init__(self, screen_size, preview_framerate):
        self.screen_size = screen_size
        self.preview_framerate = preview_framerate

        if onPi:
            self.picamera = picamera2.Picamera2()
            self.preview_config = self.picamera.create_preview_configuration({'format': 'RGB888', 'size': screen_size})
            self.photo_config = self.picamera.create_still_configuration()
            self.picamera.configure(self.preview_config)
            self.picamera.resolution = screen_size
            self.picamera.framerate = 60
            self.picamera.start()

        self.preview_frame_available = False
        self._preview_frame = None
        self._preview_running = False
        self._preview_thread = Thread(target=self.preview_loop)

        self._clock = pygame.time.Clock()
    
    def start_preview(self):
        if onPi:
            self._preview_running = True
            self._preview_thread.start()
    
    def stop_preview(self):
        self._preview_running = False
    
    def preview_loop(self):
        while self._preview_running:
            self._preview_frame = self.picamera.capture_array()
            self.preview_frame_available = True
            self._clock.tick(self.preview_framerate)
    
    def get_pygame_preview_frame(self):
        if not self.preview_frame_available:
            return None

        self.preview_frame_available = False

        return pygame.image.frombuffer(
            self._preview_frame.tostring(),
            self._preview_frame.shape[1::-1],
            "BGR")
    
    def take_photo(self):
        filename = time.strftime("%Y.%m.%d_%H-%M-%S.jpg")
        if onPi:
            self.picamera.switch_mode_and_capture_file(self.photo_config, os.path.join(PHOTOS_PATH, filename))

    def set_exposure_time(self, exposure_time_us):
        """
        Setzt die Belichtungszeit der Kamera auf einen festen Wert (in Mikrosekunden).
        exposure_time_us: int, Belichtungszeit in Mikrosekunden
        """
        if onPi:
            # self.picamera.set_controls({"ExposureTime": exposure_time_us, "AeEnable": False})
            self.picamera.controls.ExposureTime = exposure_time_us
            self.picamera.controls.AeEnable = False

    def set_auto_exposure(self):
        """
        Setzt die Belichtungszeit der Kamera auf Automatik (AE = Auto Exposure).
        """
        if onPi:
            # self.picamera.set_controls({"AeEnable": True})
            self.picamera.still_configuration.controls.AeEnable = True
    
    def set_color_gains(self, red, blue):
        if onPi:
            self.picamera.controls.ColourGains = (red, blue)