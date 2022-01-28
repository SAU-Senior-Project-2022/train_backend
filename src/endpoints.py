from flask_cors import CORS
import database
import data
from flask import jsonify, request, Flask, current_app, Response, render_template
from os.path import exists
from flask_restful import Resource, Api
import json
from sys import stderr

app = Flask(__name__)
CORS(app)
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
        print(request.json)
        data = request.json.get('state')
        state = database.getState(station_id).state
        print(state)
        if (data == None):
            return jsonify({'error': "Missing json key: 'state'", 'correct': {"state": "1|0"}})
        if int(state) != int(data):
            resp = database.setState(station_id, data)
            return jsonify(resp)
        else:
            return {"success": True}
    
class history(Resource):
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
        return jsonify(json.loads(json.dumps(resp, cls=data.station.StationEncoder)))
        # if (resp is not None):
        #     return jsonify(json.loads(json.dumps(resp, cls=data.history.HistoryEncoder)))
        #     retu
    def post(self, station_id):
        if (station_id == 'new'):
            data = request.json
            if ((data.get('latitude') == None) or (data.get('longitude') == None)):
                return jsonify({'error': "Did not receive all expected JSON fields", 'correct': {"latitude": "*location*", "longitude": "*location*"}})
            resp = database.insert_new_station(data.get('latitude'), data.get('longitude'), data.get('title'))
            return jsonify(resp)
        else:
            return 404

class locationList(Resource):
    """deals with `GET` to get list of locations of stations

    Args:
        Resource (flask-restx.Resouce): imported from flask-restx
    """

    def get(self):
        resp = database.getStationList()
        return jsonify(json.loads(json.dumps(resp, cls=data.station.StationEncoder)))

class createStationSite(Resource):
    """deals with rendering the basic location creation site

    Args:
        Resource (flask-restx.Resouce): imported from flask-restx
    """
    def get(self):
        #return send_from_directory('static/new', 'frontEnd.html')
        return Response(render_template('station_create.html'))

class createStateSite(Resource):
    """deals with rendering the basic location creation site

    Args:
        Resource (flask-restx.Resouce): imported from flask-restx
    """
    def get(self):
        #return send_from_directory('static/new', 'frontEnd.html')
        return Response(render_template('state_create.html'))

class documentationSite(Resource):
    """deals with rendering the basic location creation site

    Args:
        Resource (flask-restx.Resouce): imported from flask-restx
    """

    def get(self):
        return current_app.send_static_file('documentation.html')
