#!/usr/bin/env python3

import time

import bar_panel.hardware as hardware
import bar_panel.networking as networking
import state

if __name__ == "__main__":
    hardware.init()
    rgb_led = hardware.RgbLed()
    akk_state = state.CurrentAKKState()
    buttons = [
            hardware.AKKClosedButton(rgb_led, akk_state),
            hardware.AKKOpenNoServiceButton(rgb_led, akk_state),
            hardware.AKKOpenSelfServiceButton(rgb_led, akk_state),
            hardware.AKKOpenFullServiceButton(rgb_led, akk_state)
            ]
    server = networking.init(akk_state)
    
    rgb_led.animate_no_state()

    print("Initalized bar_panel")
    
    while True:
        for button in buttons:
            button.check()
        rgb_led.animate()

        time.sleep(0.01)

    server.shutdown()
