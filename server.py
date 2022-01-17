"""
    Server for Train Backend. This is intedned to be imported. See `start_server`
"""
from flask import Flask
from flask_cors import CORS # CORS
from flask_restful import Api # Provides API docs
import database
import endpoints
import random

app = Flask(__name__)
api = Api(app)

def seed_database():
    station_ids = []
    for i in range(22):
        station_id = database.insert_new_station(123123,12341234)
        print(station_id)
        station_ids.append(station_id)
    for i in station_ids:
        for j in range(22):
            database.setState(i, bool(random.getrandbits(1)))

def start_server(ip: str=None, port: int=5000, debug: bool=False, https: bool=True, certPath: str=None, keyPath: str=None, seed: bool=None) -> bool:
    """Starts the http server

    Args:
        ip (str, optional): IP address server binds to. Defaults to "0.0.0.0".
        port (int, optional): Port server binds to. Defaults to 5000.
        debug (bool, optional): Debug mode of Flask server. Defaults to False.
        https (bool, optional): If `True`, server will run over HTTPS. Defaults to True.
        certPath (str, optional): Path to certificate. if not provide, self signed certificate will be used. Defaults to None.
        keyPath (str, optional): Path to key. If not privided, key will be provided through flask-talisman. Defaults to None.

    Returns:
        bool: Always returns `True`
    """
    global api
    # Setup ip and port, using `None` in function declairation to be more compatible with argparser
    if (ip == None):
        ip = "0.0.0.0"
    if (port == None):
        port = 5000

    # Connect to database
    database.connect("0.0.0.0")
    
    # Assign classes to endpoints    
    api.add_resource(endpoints.State, '/state/<station_id>')
    api.add_resource(endpoints.History, '/history/<station_id>')
    api.add_resource(endpoints.LocationGet, '/location/<station_id>')
    api.add_resource(endpoints.LocationPost, '/location/new')

    #app.secret_key = os.urandom(24)
    
    # Seed database
    
    if (seed):
        seed_database()
    # Run server
    if (https):
        CORS(app)
        if (certPath == None or keyPath == None):
            app.run(debug=debug, host=ip, port=port)
        else:
            app.run(debug=debug, host=ip, port=port, ssl_context=(certPath, keyPath))
    else:
        app.run(debug=debug, host=ip, port=port)
    return True


if __name__ == "__main__":
    start_server()
