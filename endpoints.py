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
        return jsonify(json.loads(json.dumps(resp, cls=data.history.HistoryEncoder)))
    
    def post(self, station_id):
        data = request.json.get('state')
        if (data == None):
            return jsonify({'error': "Missing json key: 'state'", 'correct': {"state": "true|false"}})
        resp = database.setState(station_id, data)
        return jsonify(resp)
    
class sistory(Resource):
    """deals with `GET` for the history of a station

    Args:
        Resource (flask-restx.Resouce): imported from flask-restx
    """
    def get(self, station_id):
        resp = database.getHistory(station_id)
        return jsonify(json.loads(json.dumps(resp, cls=data.history.HistoryEncoder)))
    
class location(Resource):
    """deals with `GET` and `POST` for the location of a station

    Args:
        Resource (flask-restx.Resouce): imported from flask-restx
    """
    def get(self, station_id):
        resp = database.getStation(station_id)
        return jsonify(json.loads(json.dumps(resp, cls=data.history.HistoryEncoder)))
    def post(self):
        data = request.json
        if ((data.get('latitude') == None) or (data.get('longitude') == None)):
            return jsonify({'error': "Did not receive all expected JSON fields", 'correct': {"latitude": "*location*", "longitude": "*location*"}})
        resp = database.insert_new_station(data.get('latitude'), data.get('longitude'))
        return jsonify(resp)
