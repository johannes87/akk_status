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
        pass

    def __init__(self, rgb_led):
        self.prev_value = None
        self.cur_value = None
        self.rgb_led = rgb_led

    def check(self):
        # use self.__class.PIN
        # compare if new value is different from old value, and 1->0 (depending on pup/down)
        # if changed, call _handle
        pass



class AKKClosedButton(Button):
    """
    Button for setting the state to: AKK is closed (no entry)
    """
    PIN = 14

    def __init__(self):
        super().__init__()

    def _handle(self):
        pass


class AKKOpenNoServiceButton(Button):
    """
    Button for setting the state to: AKK is open, but no service at all
    """
    PIN = 15

    def _handle(self):
        pass


class AKKOpenSelfServiceButton(Button):
    """
    Button for setting the state to: Self service ("Cafe Selbergroß")
    """
    PIN = 23

    def _handle(self):
        pass


class AKKOpenFullServiceButton(Button):
    """
    Button for setting the state to: AKK is selling stuff at the counter
    """
    PIN = 24

    def __handle(self):
        pass
