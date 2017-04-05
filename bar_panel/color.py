import neopixel
import colorsys


# TODO make class abstract
class Color:
    def __init__(self):
        pass      

    def to_neopixel(self):
        self.neopixel = neopixel.Color(self.red, self.green, self.blue)

class RGBColor(Color):
    def __init__(self, red, green, blue):
        self.set_rgb(red, green, blue)

    def set_rgb(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

        (self.hue, self.saturation, self.value) = colorsys.rgb_to_hsv(
                self.red, self.green, self.blue)

        self.to_neopixel()

class HSVColor(Color):
    def __init__(self, hue, saturation, value):
        self.set_hsv(hue, saturation, value)

    def set_hsv(self, hue, saturation, value):
        self.hue = hue
        self.saturation = saturation
        self.value = value

        (self.red, self.green, self.blue) = colorsys.hsv_to_rgb(
                self.hue, self.saturation, self.value)

        self.to_neopixel()

        
red = RGBColor(255, 0, 0)
green = RGBColor(0, 255, 0)
orange = RGBColor(255, 128, 0)
yellow = RGBColor(255, 255, 0)
