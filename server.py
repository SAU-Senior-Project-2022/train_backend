"""
    Server for Train Backend. This is intended to be imported. See `start_server`
"""
from flask_cors import CORS # CORS
import database
import endpoints

app = Flask(__name__)
api = Api(app)

station_ids = []
def seed_database():
    for i in range(22):
        station_id = database.insert_new_station(123123,12341234)
        print(station_id)
        station_ids.append(station_id)
    for i in station_ids:
        for j in range(22):
            database.setState(i.get('station_id'), int(random.getrandbits(1)))

def start_server(ip: str=None, port: int=5000, debug: bool=False, https: bool=True, certPath: str=None, keyPath: str=None, seed: bool=None, username: str="root", password: str="", fresh_migration: bool=None) -> bool:
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
