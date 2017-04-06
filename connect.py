#!/usr/bin/env python3

import socket
import time

from state import AKKState
import config

RECONNECT_DELAY = 5

def update_state(akk_state):
    print(akk_state)
    # TODO: database update here

if __name__ == '__main__':
    (bar_raspberry_host, bar_raspberry_port) = config.get_bar_raspberry_host_port()

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            print("Connecting to {}:{}".format(bar_raspberry_host, bar_raspberry_port))
            sock.settimeout(1.0)
            try:
                sock.connect((bar_raspberry_host, bar_raspberry_port))
            except (ConnectionRefusedError, socket.timeout, OSError):
                print("Connection failed, retrying after {} seconds".format(RECONNECT_DELAY))
                time.sleep(RECONNECT_DELAY)
                continue
            
            # there mustn't be a timeout while doing sockfile.readline()
            sock.settimeout(None)

            with sock.makefile() as sockfile:
                while True:
                    akk_state_str = sockfile.readline().strip()
                    if akk_state_str == '':
                        break
                    akk_state = AKKState[akk_state_str]
                    update_state(akk_state)

            print("Connection lost, retrying after {} seconds".format(RECONNECT_DELAY))
            time.sleep(RECONNECT_DELAY)
