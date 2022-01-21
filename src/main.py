#!/usr/local/bin/python
import server
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser(description="Runs a server that provides the backend for trains.")
    
    parser.add_argument("--ip", dest="ip", default="0.0.0.0", \
        help="Specify the ip for the server. Default is 0.0.0.0.", required=False)
    parser.add_argument("--port", dest="port", default=5000, \
        help="Specify the port for the server. Default is 5000.", required=False, type=int)
    
    parser.add_argument("--username", dest="user", default="root", \
        help="Provide an username for the database", required=False)
    parser.add_argument("--password", dest="password", default="", \
        help="Provide an password for the database. \
        If not provided, it is provided by the server.", required=False)
    parser.add_argument("--db-name", dest="db_name", default="train", \
        help="Sets the database name. Defaults to \"train\"", required=False)
    parser.add_argument("--db-url", dest="db_url", default="localhost", \
        help="Sets the database url. Defaults to \"localhost\"", required=False)
    parser.add_argument("--db-port", dest="db_port", default=3306, \
        help="Sets the database port. Defaults to 3306", required=False)
    
    parser.add_argument("--http", dest="http", default=False, \
        help="The server will run over http", required=False, action="store_true")
    parser.add_argument("--cert-file", dest="cert", default=None, \
        help="Provide the path to the certificate file for \
        the server. If not provided, it is provided by the server.", required=False)
    parser.add_argument("--key-file", dest="key", default=None, \
        help="Provide the path to the key file for the server. \
        If not provided, it is provided by the server.", required=False)
    
    parser.add_argument("--debug", dest="debug", default=False, \
        help="The server will be in debug mode", required=False, \
        action="store_true")
    parser.add_argument("--fresh", dest="fresh", default=False, \
        help="Will empty the database. Requires --debug flag.", required=False, \
        action="store_true")
    parser.add_argument("--seed", dest="seed", default=False, \
        help="Will reseed the database with random values. \
        Requires --debug flag.", required=False, action="store_true")
    
    args = parser.parse_args()
    server.start_server(
        ip=args.ip, port=args.port, 
        username=args.user, password=args.password, database_name=args.db_name, db_url=args.db_url, db_port=int(args.db_port),
        http=args.http, certPath=args.cert, keyPath=args.key,
        debug=args.debug, seed=args.seed, fresh_migration=args.fresh)
else:
    server.start_server()