# TODO: was passiert wenn knopf nicht lang genug gedrueckt wird?

import RPi.GPIO as GPIO
from neopixel import *

import state

class RgbLed:
    LED_COUNT      = 1       # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

    def __init__(self):
        self.strip = Adafruit_NeoPixel(
                RgbLed.LED_COUNT, 
                RgbLed.LED_PIN, 
                RgbLed.LED_FREQ_HZ, 
                RgbLed.LED_DMA, 
                RgbLed.LED_INVERT, 
                RgbLed.LED_BRIGHTNESS)
        self.strip.begin()
    
    def set_color(self, color):
        # TODO: tweening between current color and new color
        self.strip.setPixelColor(0, color)
        self.strip.show()


class Button:
    def __init__(self, rgb_led, state):
        GPIO.setup(self.__class__.PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.prev_pin_input = None
        self.rgb_led = rgb_led
        self.state = state

    def check(self):
        pin_input = GPIO.input(self.__class__.PIN)
        
        if self.prev_pin_input is not None\
                and self.prev_pin_input == 1\
                and pin_input == 0:
            self._handle()
        
        self.prev_pin_input = pin_input


class AKKClosedButton(Button):
    """
    Button for setting the state to: AKK is closed (no entry)
    """
    PIN = 14

    def _handle(self):
        red = Color(255, 0, 0)
        self.rgb_led.set_color(red)
        self.state.set_state(state.AKKState.CLOSED)


class AKKOpenNoServiceButton(Button):
    """
    Button for setting the state to: AKK is open, but no service at all
    """
    PIN = 15

    def _handle(self):
        orange = Color(255, 128, 0)
        self.rgb_led.set_color(orange)
        self.state.set_state(state.AKKState.OPEN_NO_SERVICE)


class AKKOpenSelfServiceButton(Button):
    """
    Button for setting the state to: Self service ("Cafe Selbergroß")
    """
    PIN = 23

    def _handle(self):
        yellow = Color(255, 255, 0)
        self.rgb_led.set_color(yellow)
        self.state.set_state(state.AKKState.OPEN_SELF_SERVICE)


class AKKOpenFullServiceButton(Button):
    """
    Button for setting the state to: AKK is selling stuff at the counter
    """
    PIN = 24

    def _handle(self):
        green = Color(0, 255, 0)
        self.rgb_led.set_color(green)
        self.state.set_state(state.AKKState.OPEN_FULL_SERVICE)


def init():
    """
    Global hardware initialization for all button-related functionality
    """
    GPIO.setmode(GPIO.BCM)
