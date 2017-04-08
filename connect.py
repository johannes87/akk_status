#!/usr/bin/env python3

import socket
import time

from state import AKKState
import config

RECONNECT_DELAY = 5

def update_state(akk_state):
    print(akk_state)
    # TODO: database update here


def set_keepalive_linux(sock, after_idle_sec=1, interval_sec=3, max_fails=5):
    """Set TCP keepalive on an open socket.

    It activates after 1 second (after_idle_sec) of idleness,
    then sends a keepalive ping once every 3 seconds (interval_sec),
    and closes the connection after 5 failed ping (max_fails), or 15 seconds
    """
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, after_idle_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, interval_sec)
    sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, max_fails)

if __name__ == '__main__':
    (bar_raspberry_host, bar_raspberry_port) = config.get_bar_raspberry_host_port()

    while True:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            set_keepalive_linux(sock)

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
                    try:
                        akk_state_str = sockfile.readline().strip()
                    except Exception as e:
                        print("Exception in sockfile.readline(): {}".format(e))
                        break

                    if akk_state_str == '':
                        break
                    akk_state = AKKState[akk_state_str]
                    update_state(akk_state)

            print("Connection lost, retrying after {} seconds".format(RECONNECT_DELAY))
            time.sleep(RECONNECT_DELAY)
