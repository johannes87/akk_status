#!/usr/bin/env python3

import socketserver
import threading
import sys
import time
import functools


import hardware
import state

BUTTON_DELAY = 0.2 # TODO: put somewhere else?

state = state.State() # FIXME: this shouldn't be global

class StateTCPHandler(socketserver.StreamRequestHandler):
    def send_state(self):
        self.wfile.write(str(self.server.state.get_state_value()) + "\r\n")

    def handle(self):
        prev_state_value = None

        while True:
            try:
                # send state on new connection
                # if prev_state_value is None:
                #     self.send_state()
                # elif prev_state_value != self._state.get_state_value():
                #     self.send_state()
                # 
                # prev_state_value = self._state.get_state()
                # self.send_state()
                # print(self.server.state.get_state_value())
                print(state.get_state_value())
                time.sleep(4)

            except BrokenPipeError:
                break


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


if __name__ == "__main__":
    hardware.init()
    rgb_led = hardware.RgbLed()
    buttons = [
            hardware.AKKClosedButton(rgb_led, state),
            hardware.AKKOpenNoServiceButton(rgb_led, state),
            hardware.AKKOpenSelfServiceButton(rgb_led, state),
            hardware.AKKOpenFullServiceButton(rgb_led, state)
            ]

    HOST, PORT = "localhost", 9999
    socketserver.TCPServer.allow_reuse_address = True

    server = ThreadingTCPServer((HOST, PORT), StateTCPHandler)
    server.state = state # HACK: there's no easy way to pass a param to StateTCPHandler
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    
    while True:
        for button in buttons:
            button.check()

        print('state=', state.get_state_value())
        time.sleep(BUTTON_DELAY)

    server.shutdown()
