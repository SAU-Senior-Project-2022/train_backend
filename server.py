"""
    Server for Train Backend. This is intended to be imported. See `start_server`
"""
from flask_cors import CORS # CORS
import database
import endpoints

def start_server(
    ip: str="0.0.0.0", port: int=5000,
    username: str="root", password: str="", database_name: str="train", db_url: str="localhost",
    http: bool=False, certPath: str=None, keyPath: str=None,
    debug: bool=False, seed: bool=False, fresh_migration: bool=False) -> None:
    """Starts the http server

    Args:
        ip (str, optional): IP address server binds to. Defaults to "0.0.0.0".
        port (int, optional): Port server binds to. Defaults to 5000.
        username (str, optional): Username for database. Defaults to "root".
        password (str, optional): Password for database. Defaults to "".
        database_name (str, optional): Name of database to use. Defaults to "train".
        db_url (str, optional): URL of the database to use. Defaults to "localhost".
        http (bool, optional): [If `True`, server will run over HTTP. Defaults to False.
        certPath (str, optional): Path to certificate. if not provide, self signed certificate \
            will be used. Defaults to None.
        keyPath (str, optional): Path to key. If not provided, key will be provided \
            through flask-talisman. Defaults to None.Path to key. If not provided, \
            key will be provided through flask-talisman. Defaults to None.
        debug (bool, optional): Debug mode of Flask server. Defaults to False.
        seed (bool, optional): Whether database should be seeded. Defaults to False.
        fresh_migration (bool, optional): Whether or not to create fresh database. \
            Defaults to False.
    """
    # Connect to database
    database.connect(url=db_url, username=username, password=password, 
        database=database_name, fresh_migrate=(fresh_migration and debug))
    
    # Assign classes to endpoints    
    endpoints.api.add_resource(endpoints.state, '/state/<station_id>')
    endpoints.api.add_resource(endpoints.history, '/history/<station_id>')
    endpoints.api.add_resource(endpoints.location, '/location/<station_id>')
    endpoints.api.add_resource(endpoints.locationList, '/location')

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
