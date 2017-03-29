#!/usr/bin/env python3

import socket
import time

from state import AKKState

BAR_RASPBERRY_HOST = "raspberrypi"
BAR_RASPBERRY_PORT = 9999
RECONNECT_DELAY = 5

def update_state(akk_state):
    print(akk_state)
    # TODO: database update here

if __name__ == '__main__':
    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            print("Connecting to {}:{}".format(BAR_RASPBERRY_HOST, BAR_RASPBERRY_PORT))
            try:
                sock.connect((BAR_RASPBERRY_HOST, BAR_RASPBERRY_PORT))
            except ConnectionRefusedError:
                print("Connection refused, retrying after {} seconds".format(RECONNECT_DELAY))
                time.sleep(RECONNECT_DELAY)
                continue

            with sock.makefile() as sockfile:
                while True:
                    akk_state_str = sockfile.readline().strip()
                    if akk_state_str == '':
                        break
                    akk_state = AKKState[akk_state_str]
                    update_state(akk_state)

            print("Connection lost, retrying after {} seconds".format(RECONNECT_DELAY))
            time.sleep(RECONNECT_DELAY)
