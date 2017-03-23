#!/usr/bin/env python3

import socketserver
import threading
import sys

class MyTCPHandler(socketserver.StreamRequestHandler):
    def handle(self):
        while True:
            data = self.rfile.readline().strip()
            print("{} wrote:".format(self.client_address[0]))
            print(data)
            self.wfile.write(data.upper())


class ThreadingTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999
    socketserver.TCPServer.allow_reuse_address = True

    # Create the server, binding to localhost on port 9999
    with ThreadingTCPServer((HOST, PORT), MyTCPHandler) as server:
        server_thread = threading.Thread(target=server.serve_forever)
        # Exit the server thread when the main thread terminates
        server_thread.daemon = True
        server_thread.start()

        sys.stdin.readline() 

        server.shutdown()


