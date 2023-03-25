"""Small example OSC server

This program listens to several addresses, and prints some information about
received packets.
"""
import argparse

from pythonosc.dispatcher import Dispatcher
from pythonosc import osc_server


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--ip",
        default="localhost", help="The ip to listen on")
    parser.add_argument("--port",
        type=int, default=9001, help="The port to listen on")
    args = parser.parse_args()

    dispatcher = Dispatcher()
    dispatcher.map("/avatar/parameters/*", print)

    server = osc_server.ThreadingOSCUDPServer(
        (args.ip, args.port), dispatcher)
    print("Serving on {}".format(server.server_address))
    # server.serve_forever()
    server.server_activate
    server.timeout = 0.1
    while True:
        server.handle_request()