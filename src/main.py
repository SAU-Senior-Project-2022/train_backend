#!/usr/local/bin/python
import server
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser(description="Runs a server that provides the backend for trains.")
    
    parser.add_argument("--ip", dest="ip", default="0.0.0.0", \
        help="Specify the ip for the server. Default is 0.0.0.0.", required=False)
    parser.add_argument("--port", dest="port", default=5000, \
        help="Specify the port for the server. Default is 5000.", required=False, type=int)
    
    parser.add_argument("--db-name", dest="db_name", default="train", \
        help="Sets the database name. Defaults to \"train\"", required=False)
    
    parser.add_argument("--http", dest="http", default=False, \
        help="The server will run over http", required=False, action="store_true")
    parser.add_argument("--cert-file", dest="cert", default=None, \
        help="Provide the path to the certificate file for \
        the server. If not provided, it is provided by the server.", required=False)
    parser.add_argument("--key-file", dest="key", default=None, \
        help="Provide the path to the key file for the server. \
        If not provided, it is provided by the server.", required=False)
    
    parser.add_argument("--fresh", dest="fresh", default=False, \
        help="Will empty the database.", required=False, \
        action="store_true")
    
    args = parser.parse_args()
    server.start_server(
        ip=args.ip, port=args.port, 
        database_name=args.db_name,
        http=args.http, certPath=args.cert, keyPath=args.key,
        fresh_migration=args.fresh)
else:
    server.start_server()