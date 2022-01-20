"""
    Server for Train Backend. This is intended to be imported. See `start_server`
"""
from flask_cors import CORS # CORS
import database
import endpoints

def start_server(
    ip: str="0.0.0.0", port: int=5000,
    username: str="root", password: str="",
    http: bool=False, certPath: str=None, keyPath: str=None,
    debug: bool=False, seed: bool=False, fresh_migration: bool=False) -> None:
    """Starts the http server

    Args:
        ip (str, optional): IP address server binds to. Defaults to "0.0.0.0".
        port (int, optional): Port server binds to. Defaults to 5000.
        debug (bool, optional): Debug mode of Flask server. Defaults to False.
        https (bool, optional): If `True`, server will run over HTTPS. Defaults to True.
        certPath (str, optional): Path to certificate. if not provide, self signed certificate will be used. Defaults to None.
        keyPath (str, optional): Path to key. If not provided, key will be provided through flask-talisman. Defaults to None.

    Returns:
        bool: Always returns `True`
    """

    #settings = 
    # Connect to database
    database.connect(url=ip, username=username, password=password, 
        fresh_migrate=(fresh_migration and debug) )
    
    # Assign classes to endpoints    
    endpoints.api.add_resource(endpoints.state, '/state/<station_id>')
    endpoints.api.add_resource(endpoints.history, '/history/<station_id>')
    endpoints.api.add_resource(endpoints.locationGet, '/location/<station_id>')
    endpoints.api.add_resource(endpoints.locationPost, '/location/new')

    # Seed database    
    if (seed and debug):
        database.seed_database()

    # Run server
    if (http):
        endpoints.app.run(debug=debug, host=ip, port=port)
    else:
        CORS(endpoints.app)
        if (certPath == None or keyPath == None):
            endpoints.app.run(debug=debug, host=ip, port=port)
        else:
            endpoints.app.run(debug=debug, host=ip, port=port, ssl_context=(certPath, keyPath))


if __name__ == "__main__":
    print("Please run from main.py")
