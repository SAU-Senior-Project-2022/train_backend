from flask import Flask, json, jsonify, request
import flask_cors
from database import *
#database = None
app = Flask(__name__)

#gets the 
@app.route('/state/<stationId>', methods=['GET'])
def getStationState(stationId):
    return jsonify(getState(stationId))

@app.route('/history/<stationId>', methods=['GET'])
def getStationHistory(stationId):
    return jsonify(getHistory(stationId))

@app.route('/location/<stationId>', methods=['GET'])
def getStationLocation(stationId):
    return jsonify(getStation(stationId))

@app.route('/state/set', methods=['POST'])
def setStationState():
    data = request.json
    return jsonify(setState(data.get('station_id'), data.get('state')))




def start_server():
    # if database == None:
    #     connectDb()
    CORS(app)
    #app.secret_key = os.urandom(24)
    app.run(debug=True, host="0.0.0.0")


if __name__ == "__main__":
    start_server()