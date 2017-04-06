import socketserver
import threading
import time

import config

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

def init(akk_state):
    socketserver.TCPServer.allow_reuse_address = True
    
    (_, listen_port) = config.get_bar_raspberry_host_port()
    server = ThreadingTCPServer(("0.0.0.0", listen_port), StateTCPHandler)

    # see https://stackoverflow.com/questions/6875599/with-python-socketserver-how-can-i-pass-a-variable-to-the-constructor-of-the-han
    server.akk_state = akk_state
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
