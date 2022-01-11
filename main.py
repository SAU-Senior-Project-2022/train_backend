#!/bin/env python
import server
import argparse

if (__name__ == "__main__"):
    parser = argparse.ArgumentParser(description="Runs a server that provides the backend for trains.")
    parser.add_argument("--ip", dest="ip", help="Specify the ip for the server. Default is 0.0.0.0.", required=False)
    parser.add_argument("--port", dest="port", help="Specify the port for the server. Default is 5000.", required=False, type=int)
    parser.add_argument("--debug", dest="debug", help="The server will be in debug mode", required=False, action="store_true")
    parser.add_argument("--http", dest="http", help="The server will run over http", required=False, action="store_true")
    parser.add_argument("--cert-file", dest="cert", 
                        help="Provide the path to the certificate file for \
                        the server. If not provided, it is provided by the server.", required=False)
    parser.add_argument("--key-file", dest="key", 
                        help="Provide the path to the key file for the server. \
                        If not provided, it is provided by the server.", required=False)
    args = parser.parse_args()
    server.start_server(ip=args.ip, port=args.port, debug=args.debug, https=not args.http, certPath=args.cert, keyPath=args.key)