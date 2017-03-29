#!/usr/bin/env python3

import socketserver
import threading
import sys
import time
import functools

import hardware
import state

BUTTON_DELAY = 0.2

class StateTCPHandler(socketserver.StreamRequestHandler):
    def send_state(self):
        st = self.server.akk_state.get_state()
        if st is None:
            print("No state set; not sending anything")
            return
        self.wfile.write(bytes(str(st.name) + '\r\n', 'UTF-8'))

    def handle(self):
        prev_state = None

        while True:
            try:
                # send state on new connection
                if prev_state is None:
                    self.send_state()
                elif prev_state != self.server.akk_state.get_state():
                    self.send_state()
                
                prev_state = self.server.akk_state.get_state()
                time.sleep(1)

            except BrokenPipeError:
                break


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


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

    HOST, PORT = "localhost", 9999
    socketserver.TCPServer.allow_reuse_address = True

    server = ThreadingTCPServer((HOST, PORT), StateTCPHandler)
    # see https://stackoverflow.com/questions/6875599/with-python-socketserver-how-can-i-pass-a-variable-to-the-constructor-of-the-han
    server.akk_state = akk_state
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    while True:
        for button in buttons:
            button.check()

        time.sleep(BUTTON_DELAY)

    server.shutdown()
