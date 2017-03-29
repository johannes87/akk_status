#!/usr/bin/env python3

import time

import hardware
import state
import networking

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

    while True:
        for button in buttons:
            button.check()
        time.sleep(BUTTON_DELAY)

    server.shutdown()
