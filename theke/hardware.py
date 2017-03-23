# TODO: was passiert wenn knopf nicht lang genug gedrueckt wird?

import RPi.GPIO as GPIO

class RgbLed:
    PIN = 18

    def __init__(self):
        pass
    
    def set_color(self, color):
        # TODO: tweening between current color and new color
        pass


class Button:
    @staticmethod
    def init_hardware():
        """
        Global hardware initialization for all button-related functionality
        """
        GPIO.setmode(GPIO.BCM)

    def __init__(self, rgb_led):
        GPIO.setup(self.__class__.PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        self.prev_pin_input = None
        self.rgb_led = rgb_led

    def check(self):
        pin_input = GPIO.input(self.__class__.PIN)
        
        if self.prev_pin_input is not None \
                and self.prev_pin_input == 1\
                and pin_input == 0:
            self._handle()
        
        self.prev_pin_input = pin_input


class AKKClosedButton(Button):
    """
    Button for setting the state to: AKK is closed (no entry)
    """
    PIN = 14

    def __init__(self, rgb_led):
        super().__init__(rgb_led)

    def _handle(self):
        print("akk zu")


class AKKOpenNoServiceButton(Button):
    """
    Button for setting the state to: AKK is open, but no service at all
    """
    PIN = 15

    def __init__(self, rgb_led):
        super().__init__(rgb_led)

    def _handle(self):
        print("kein service")


class AKKOpenSelfServiceButton(Button):
    """
    Button for setting the state to: Self service ("Cafe Selbergroß")
    """
    PIN = 23

    def __init__(self, rgb_led):
        super().__init__(rgb_led)

    def _handle(self):
        print("cafe selbergrosz")


class AKKOpenFullServiceButton(Button):
    """
    Button for setting the state to: AKK is selling stuff at the counter
    """
    PIN = 24

    def __init__(self, rgb_led):
        super().__init__(rgb_led)

    def _handle(self):
        print("thekenbetrieb")
