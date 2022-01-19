import database
import data
import json
from flask import jsonify, request, Response, Flask
from flask_restful import Resource, reqparse, Api
from sys import stderr

app = Flask(__name__)
api = Api(app)

# Create classes to handle requests
class state(Resource):
    """deals with `GET` and `POST` for the state of a station

    Args:
        Resource (flask-restx.Resouce): imported from flask-restx
    """        
    def get(self, station_id):
        resp = database.getState(station_id)
        # if (resp.get("error") != None):
        #     print(f"Error: {resp.get('error')}", file=stderr)
        return jsonify(json.loads(json.dumps(resp, cls=data.history.HistoryEncoder)))
    
    def post(self, station_id):
        parser = reqparse.RequestParser()
        parser.add_argument('state', type=bool, help='State of the station')
        data = request.json
        #print(data.get('state') == None)
        #args = parser.parse_args()
        # print(type(args))
        # print(args)
        if (data.get('state') == None):
            return Response(json.dumps({'error': "Missing json key: 'state'", 'correct': {"state": "true|false"}}), status=422, mimetype="application/json" )
            pass
        resp = database.setState(station_id, args.get('station_id'))
        if (resp.get("error") != None):
            print(f"Error: {resp.get('error')}", file=stderr)
            return Response(json.dumps({'error': resp.get('error'), 'correct': {"state": "true|false"}}), status=422, mimetype="application/json" )
        return jsonify(resp)
    
class sistory(Resource):
    """deals with `GET` for the history of a station

    Args:
        Resource (flask-restx.Resouce): imported from flask-restx
    """
    def get(self, station_id):
        resp = database.getHistory(station_id)
        if (resp[0].get('error') != None):
            print(f"Error: {resp[0].get('error')}", file=stderr)
        return jsonify(resp)
    
class location(Resource):
    """deals with `GET` and `POST` for the location of a station

    Args:
        Resource (flask-restx.Resouce): imported from flask-restx
    """
    def get(self, station_id):
        resp = database.getStation(station_id)
        if (resp.get('error') != None):
            print(f"Error: {resp.get('error')}", file=stderr)
        return jsonify(resp)
class LocationPost(Resource):
    """deals with `POST` for the location of a station

    Args:
        Resource (flask-restx.Resouce): imported from flask-restx
    """
    def post(self):
        data = request.json
        print(data.get('latitude'))
        
        # json_data = request.get_json(force=True) ## TO TRY
        if ((data.get('latitude') == None) or (data.get('longitude') == None)):
            print("Error: All JSON fields expected not received", file=stderr)
            return Response(json.dumps({'error': "Did not receive all expected JSON fields", 'correct': {"latitude": "*location*", "longitude": "*location*"}}), status=422, mimetype="application/json" )
        resp = database2.insert_new_station(data.get('latitude'), data.get('longitude'))
        if (resp.get('error') != None):
            print(f"Error: {resp.get('error')}", file=stderr)
        return jsonify(resp)
