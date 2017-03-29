#!/usr/bin/env python3

import time

import bar_panel.hardware as hardware
import bar_panel.networking as networking
import state

BUTTON_DELAY = 0.2

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
    
    # trigger closed-button event on start (default state)
    # TODO: rainbow colors when no state is set, to notify user that PI has rebooted and no state is set
    buttons[0]._handle()

    while True:
        for button in buttons:
            button.check()
        time.sleep(BUTTON_DELAY)

    server.shutdown()
