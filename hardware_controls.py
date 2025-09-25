try:
    import RPi.GPIO as GPIO
    onPi = True
except:
    onPi = False
import time
from threading import Thread

# Rotary encoder pins
PIN_CLOCK = 12
PIN_DT = 10
PIN_SW = 8

# Back button pin
PIN_BUTTON = 40

EVENT_BUTTON = "button"
EVENT_TRIGGER = "trigger"
EVENT_UP = "up"
EVENT_DOWN = "down"
EVENT_CW = "cw"
EVENT_CCW = "ccw"

BOUNCETIME = 5

ROTATION_UNKNOWN = 0
ROTATION_CW = 1
ROTATION_CCW = 2

class CameraControls:
    def __init__(self):
        if onPi:
            GPIO.setmode(GPIO.BOARD)

            GPIO.setup(PIN_CLOCK, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(PIN_DT, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            GPIO.setup(PIN_SW, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            GPIO.setup(PIN_BUTTON, GPIO.IN, pull_up_down=GPIO.PUD_UP)

            GPIO.add_event_detect(PIN_CLOCK, GPIO.BOTH, callback=self.on_clock_or_dt)
            GPIO.add_event_detect(PIN_DT, GPIO.BOTH, callback=self.on_clock_or_dt)
            
            GPIO.add_event_detect(PIN_SW, GPIO.BOTH, callback=self.on_sw, bouncetime=BOUNCETIME)

            GPIO.add_event_detect(PIN_BUTTON, GPIO.BOTH, callback=self.on_button, bouncetime=BOUNCETIME)

        self.events = []

        # I used this tutorial to understand rotary encoders.
        # https://github.com/nstansby/rpi-rotary-encoder-python
        self.state = 0
        self.rotation = ROTATION_UNKNOWN

    def on_clock_or_dt(self, pin):
        # 00 both 0
        # 10 clk 1
        # 01 dt 1
        # 11 both 1
        if onPi:
            new_state = 10 * GPIO.input(PIN_DT) + GPIO.input(PIN_CLOCK)

        if self.state == 0:
            if new_state == 1:
                self.rotation = ROTATION_CW
            elif new_state == 10:
                self.rotation = ROTATION_CCW
        elif self.state == 11:
            if self.rotation == ROTATION_UNKNOWN:
                if new_state == 1:
                    self.rotation = ROTATION_CCW
                elif new_state == 10:
                    self.rotation = ROTATION_CW

        if self.state != 0 and new_state == 0:
            if self.rotation == ROTATION_CW:
                self.events.append((EVENT_TRIGGER, EVENT_CW))
            elif self.rotation == ROTATION_CCW:
                self.events.append((EVENT_TRIGGER, EVENT_CCW))
            
            self.rotation = ROTATION_UNKNOWN
        
        self.state = new_state
            

    def on_sw(self, pin):
        if GPIO.input(PIN_SW):
            self.events.append((EVENT_TRIGGER, EVENT_UP))
        else:
            self.events.append((EVENT_TRIGGER, EVENT_DOWN))

    def on_button(self, pin):
        if GPIO.input(PIN_BUTTON):
            self.events.append((EVENT_BUTTON, EVENT_UP))
            print("BUTTON UP")
        else:
            self.events.append((EVENT_BUTTON, EVENT_DOWN))
            print("BUTTON DOWN")

    def get_events(self):
        events = list(self.events)
        self.events = []

        return events
    
    def quit(self):
        if onPi:
            GPIO.cleanup()