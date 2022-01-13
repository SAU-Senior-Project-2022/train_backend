"""
    Server for Train Backend. This is intedned to be imported. See `start_server`
"""
from os import stat
from flask import Flask, jsonify, request, Response
import flask
from flask_cors import CORS                     # CORS
from flask_restx import Api, Resource, fields, reqparse   # Provides API docs
import flask_restx
import json
from werkzeug.wrappers import response
from database import *
from sys import stderr

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
    api = Api(app)
    # Create classes to handle requests
    class State(Resource):
        """deals with `GET` and `POST` for the state of a station

        Args:
            Resource (flask-restx.Resouce): imported from flask-restx
        """        
        @api.response(200, 'Success', api.model('State_Get_Response', {'time': fields.Date, 'state': fields.Boolean}))
        def get(self, station_id):
            resp = getState(station_id)
            if (resp.get("error") != None):
                print(f"Error: {resp.get('error')}", file=stderr)
            return jsonify(resp)
        
        @api.response(200, 'Success', api.model('State_Post_Response', {'success': fields.Boolean}))
        @api.response(422, 'Malformed JSON', api.model('State_Post_Error_Response', {'error': fields.String, 'correct': fields.Nested(api.model("Error_Correct_State", {"state": fields.Boolean}))}))
        def post(self, station_id):
            parser = reqparse.RequestParser()
            parser.add_argument('state', type=bool, help='State of the station')
            args = parser.parse_args()
            print(type(args))
            print(args)
            if (args.get('state') == None):
                return Response(json.dumps({'error': "Missing json key: 'state'", 'correct': {"state": "true|false"}}), status=422, mimetype="application/json" )
                pass
            resp = setState(station_id, args.get('station_id'))
            if (resp.get("error") != None):
                print(f"Error: {resp.get('error')}", file=stderr)
                return Response(json.dumps({'error': resp.get('error'), 'correct': {"state": "true|false"}}), status=422, mimetype="application/json" )
            return jsonify(resp)
        
    class History(Resource):
        """deals with `GET` for the history of a station

        Args:
            Resource (flask-restx.Resouce): imported from flask-restx
        """
        get_response_model = api.model('History_Get_Response_Nested', {'time': fields.Date, 'state': fields.Boolean})
        @api.response(200, 'Success', api.model("History_Get_Response", {'data': fields.List(fields.Nested(get_response_model))}))
        def get(self, station_id):
            resp = getHistory(station_id)
            if (resp[0].get('error') != None):
                print(f"Error: {resp[0].get('error')}", file=stderr)
            return jsonify(resp)
        
    class LocationGet(Resource):
        """deals with `GET` for the location of a station

        Args:
            Resource (flask-restx.Resouce): imported from flask-restx
        """
        @api.response(200, "Success", api.model("Location_Get_Response", { "latitude": fields.String, "longitude": fields.String}))
        def get(self, station_id):
            resp = getStation(station_id)
            if (resp.get('error') != None):
                print(f"Error: {resp.get('error')}", file=stderr)
            return jsonify(resp)
    class LocationPost(Resource):
        """deals with `POST` for the location of a station

        Args:
            Resource (flask-restx.Resouce): imported from flask-restx
        """
        @api.response(200, "Success", api.model("Location_Post_Response", {"station_id": fields.Integer}))
        @api.response(422, 'Malformed JSON', api.model('Location_Post_Error_Response', {'error': fields.String, 'correct': fields.Nested(api.model('Location_Post_Error_Correct', {"latitude": fields.String, "longitude": fields.String}))}))
        def post(self):
            data = request.json
            
            # json_data = request.get_json(force=True) ## TO TRY
            if ((data.get('latitude') != None) or (data.get('longitude') != None)):
                print("Error: All JSON fields expected not received", file=stderr)
                return Response(json.dumps({'error': "Did not receive all expected JSON fields", 'correct': {"latitude": "*location*", "longitude": "*location*"}}), status=422, mimetype="application/json" )
            resp = insert_new_station(data.get('latitude'), data.get('longitude'))
            if (resp.get('error') != None):
                print(f"Error: {resp.get('error')}", file=stderr)
            return jsonify(resp)
    
    # Assign classes to endpoints
    api.namespace("State", "Handles GET/POST for states of stations").add_resource(State, '/<station_id>')
    api.namespace("History", "GET for history for a station").add_resource(History, '/<station_id>')
    api.namespace("Location", "Handles GET/POST for location of stations").add_resource(LocationGet, '/<station_id>')
    api.namespace("Location").add_resource(LocationPost, '/new')

    #app.secret_key = os.urandom(24)
    
    # Run server
    if (https):
        if (certPath == None or keyPath == None):
            app.run(debug=debug, host=ip, port=port)
        else:
            app.run(debug=debug, host=ip, port=port, ssl_context=(certPath, keyPath))
    else:
        app.run(debug=debug, host=ip, port=port)
    return True


if __name__ == "__main__":
    start_server()
