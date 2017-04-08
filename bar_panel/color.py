import neopixel
import colorsys

class Color:
    def __init__(self):
        # TODO make Color class abstract
        pass

    def to_neopixel(self):
        self.neopixel = neopixel.Color(
                int(self.red), 
                int(self.green), 
                int(self.blue))

    def set_rgb(self, red, green, blue):
        self.red = red
        self.green = green
        self.blue = blue

        (self.hue, self.saturation, self.value) = colorsys.rgb_to_hsv(
                self.red / 255, 
                self.green / 255, 
                self.blue / 255)

        self.to_neopixel()

    def set_hsv(self, hue, saturation, value):
        self.hue = hue
        self.saturation = saturation
        self.value = value
        
        (self.red, self.green, self.blue) = [int(x * 255) for x in colorsys.hsv_to_rgb(self.hue, self.saturation, self.value)]

        self.to_neopixel()

class RGBColor(Color):
    def __init__(self, red, green, blue):
        self.set_rgb(red, green, blue)

class HSVColor(Color):
    def __init__(self, hue, saturation, value):
        self.set_hsv(hue, saturation, value)

red = RGBColor(255, 0, 0)
green = RGBColor(0, 255, 0)
blue = RGBColor(0, 0, 255)
orange = RGBColor(255, 128, 0)
yellow = RGBColor(255, 255, 0)
purple = RGBColor(128, 0, 128)
