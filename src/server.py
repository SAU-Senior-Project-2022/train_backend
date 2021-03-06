"""
    Server for Train Backend. This is intended to be imported. See `start_server`
"""
import database
import endpoints

def start_server(
    ip: str="0.0.0.0", port: int=5000,
    database_name: str="train.db",
    http: bool=False, certPath: str=None, keyPath: str=None,
    fresh_migration: bool=False) -> None:
    """Starts the http server

    Args:
        ip (str, optional): IP address server binds to. Defaults to "0.0.0.0".
        port (int, optional): Port server binds to. Defaults to 5000.
        database_name (str, optional): Name of database to use. Defaults to "train".
        http (bool, optional): [If `True`, server will run over HTTP. Defaults to False.
        certPath (str, optional): Path to certificate. if not provide, self signed certificate \
            will be used. Defaults to None.
        keyPath (str, optional): Path to key. If not provided, key will be provided \
            through flask-talisman. Defaults to None.Path to key. If not provided, \
            key will be provided through flask-talisman. Defaults to None.
        fresh_migration (bool, optional): Whether or not to create fresh database. \
            Defaults to False.
    """
   
    database.connect(database=database_name, fresh_migrate=(fresh_migration))
    
    # Assign classes to endpoints    
    endpoints.api.add_resource(endpoints.state, '/state/<station_id>')
    #endpoints.api.add_resource(endpoints.history, '/history/<station_id>')
    endpoints.api.add_resource(endpoints.location, '/location/<station_id>')
    endpoints.api.add_resource(endpoints.locationList, '/location')
    endpoints.api.add_resource(endpoints.createStationSite, '/site/location/new')
    endpoints.api.add_resource(endpoints.createStateSite, '/site/state/new')
    endpoints.api.add_resource(endpoints.documentationSite, '/site/documentation')

    
    # Run server
    if (http):
        endpoints.app.run(debug=False, host=ip, port=port, threaded=False)
    else:
        if (certPath == None or keyPath == None):
            endpoints.app.run(debug=False, host=ip, port=port, threaded=False)
        else:
            endpoints.app.run(debug=False, host=ip, port=port, ssl_context=(certPath, keyPath), threaded=False)


if __name__ == "__main__":
    print("Please run from main.py")
