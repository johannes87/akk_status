# TODO: was passiert wenn knopf nicht lang genug gedrueckt wird?

import RPi.GPIO as GPIO
import neopixel
from enum import Enum
import copy

import bar_panel.color as color
import state

class RgbLed:
    LED_COUNT      = 1       # Number of LED pixels.
    LED_PIN        = 18      # GPIO pin connected to the pixels (must support PWM!).
    LED_FREQ_HZ    = 800000  # LED signal frequency in hertz (usually 800khz)
    LED_DMA        = 5       # DMA channel to use for generating signal (try 5)
    LED_BRIGHTNESS = 255     # Set to 0 for darkest and 255 for brightest
    LED_INVERT     = False   # True to invert the signal (when using NPN transistor level shift)

    def __init__(self):
        self.current_color = None
        # XXX: using abstract data types in python possible? 
        # (put transition_color in Animation?)
        self.transition_color = None         
        self.current_animation = None

        self.strip = neopixel.Adafruit_NeoPixel(
                RgbLed.LED_COUNT, 
                RgbLed.LED_PIN, 
                RgbLed.LED_FREQ_HZ, 
                RgbLed.LED_DMA, 
                RgbLed.LED_INVERT, 
                RgbLed.LED_BRIGHTNESS)
        self.strip.begin()
        
        # set default color
        self.set_color(color.red)
    
    def set_color(self, new_color):
        self.strip.setPixelColor(0, new_color.neopixel)
        self.strip.show()
        self.current_color = new_color

    def animate_color_transition(self, transition_color):
        self.current_animation = self.Animation.COLOR_TRANSITION
        self.transition_color = transition_color

    def animate_no_state(self):
        self.current_animation = self.Animation.NO_STATE

    def animate(self):
        def _animate_color_transition():
            CREMENT = 0.001
            DIFF_THRESHOLD = 0.002

            do_increment = (self.transition_color.hue - self.current_color.hue) > 0

            # print("_animate_color_transition: cur={}, tc={}, diff={}".format(
            #     self.current_color.hue,
            #     self.transition_color.hue,
            #     self.transition_color.hue - self.current_color.hue))

            if do_increment:
                self.set_color(color.HSVColor(
                    (self.current_color.hue + CREMENT) % 1,
                    self.current_color.saturation,
                    self.current_color.value))
            else:
                self.set_color(color.HSVColor(
                    (self.current_color.hue - CREMENT) % 1,
                    self.current_color.saturation,
                    self.current_color.value))

            do_stop = abs(self.transition_color.hue - self.current_color.hue) \
                    < DIFF_THRESHOLD

            if do_stop:
                self.current_animation = None


        def _animate_no_state():
            # rainbow animation
            new_color = color.HSVColor(
                    (self.current_color.hue + 0.005) % 1, 
                    self.current_color.saturation,
                    self.current_color.value)
            
            self.set_color(new_color)

        if self.current_animation is None:
            return
        if self.current_animation == self.Animation.NO_STATE:
            _animate_no_state()
        if self.current_animation == self.Animation.COLOR_TRANSITION:
            _animate_color_transition()

    class Animation(Enum):
        NO_STATE = 1
        COLOR_TRANSITION = 2

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
        self.rgb_led.animate_color_transition(color.red)
        self.state.set_state(state.AKKState.CLOSED)


class AKKOpenNoServiceButton(Button):
    """
    Button for setting the state to: AKK is open, but no service at all
    """
    PIN = 15

    def _handle(self):
        self.rgb_led.animate_color_transition(color.orange)
        self.state.set_state(state.AKKState.OPEN_NO_SERVICE)


class AKKOpenSelfServiceButton(Button):
    """
    Button for setting the state to: Self service ("Cafe Selbergroß")
    """
    PIN = 23

    def _handle(self):
        self.rgb_led.animate_color_transition(color.yellow)
        self.state.set_state(state.AKKState.OPEN_SELF_SERVICE)


class AKKOpenFullServiceButton(Button):
    """
    Button for setting the state to: AKK is selling stuff at the counter
    """
    PIN = 24

    def _handle(self):
        self.rgb_led.animate_color_transition(color.green)
        self.state.set_state(state.AKKState.OPEN_FULL_SERVICE)


def init():
    """
    Global hardware initialization for all button-related functionality
    """
    GPIO.setmode(GPIO.BCM)
