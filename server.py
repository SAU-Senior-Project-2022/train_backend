"""
    Server for Train Backend. This is intedned to be imported. See `start_server`
"""
from flask import Flask, jsonify, request, redirect
from flask_cors import CORS                     # CORS
from flask_restx import Api, Resource, fields   # Provides API docs
from database import *

def start_server(ip: str=None, port: int=5000, debug: bool=False, https: bool=True, certPath: str=None, keyPath: str=None) -> bool:
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

    # Create flask app
    app = Flask(__name__)
    CORS(app)
    if (https):
        @app.before_request
        def before_request():
            scheme = request.headers.get('X-Forwarded-Proto')
            if scheme and scheme == 'http' and request.url.startswith('http://'):
                url = request.url.replace('http://', 'https://', 1)
                code = 301
                return redirect(url, code=code)
    api = Api(app)
    
    # Create classes to handle requests
    class State(Resource):
        """deals with `GET` and `POST` for the state of a station

        Args:
            Resource (flask-restx.Resouce): imported from flask-restx
        """
        state_model = api.model('State_Model', {'station_id': fields.Integer, 'time': fields.Date, 'state': fields.Boolean,})
        
        @api.response(200, 'Success', api.model('Response_Model', {'state': fields.Boolean,}))
        def get(self, station_id):
            return jsonify({"state": getState(station_id)})
        def post(self, station_id):
            return jsonify(setState(station_id, request.json.get('state')))
        
    class History(Resource):
        """deals with `GET` for the history of a station

        Args:
            Resource (flask-restx.Resouce): imported from flask-restx
        """
        
        @api.marshal_with([State.state_model])
        def get(self, station_id):
            return jsonify(getHistory(station_id))
        
    class LocationGet(Resource):
        """deals with `GET` for the location of a station

        Args:
            Resource (flask-restx.Resouce): imported from flask-restx
        """
        @api.response(200, "Success", api.model("Location_Model", {"station_id": fields.Integer, "latitude": fields.String, "longitude": fields.String}))
        def get(self, station_id):
            return jsonify(getStation(station_id))
    class LocationPost(Resource):
        """deals with `POST` for the location of a station

        Args:
            Resource (flask-restx.Resouce): imported from flask-restx
        """
        def post(self):
            data = request.json
            return jsonify({"station_id": insert_new_station(data.get('latitude'), data.get('longitude'))})
    
    # Assign classes to endpoints
    api.namespace("State", "Handles GET/POST for states of stations").add_resource(State, '/<station_id>')
    api.namespace("History", "GET for history for a station").add_resource(History, '/<station_id>')
    api.namespace("Location", "Handles GET/POST for location of stations").add_resource(LocationGet, '/<station_id>')
    api.namespace("Location").add_resource(LocationPost, '/new')
    
    # Document database models
    state = api.model('State', {
        'id': fields.Integer(readonly=True, description='The task unique identifier'),
        'task': fields.String(required=True, description='The task details')
    })

    #app.secret_key = os.urandom(24)
    
    # Run server
    if (https):
        if (certPath == None or keyPath == None):
            app.run(debug=debug, host=ip, port=port, ssl_context='adhoc')
        else:
            app.run(debug=debug, host=ip, port=port, ssl_context=(certPath, keyPath))
    else:
        app.run(debug=debug, host=ip, port=port)
    return True


if __name__ == "__main__":
    start_server()
