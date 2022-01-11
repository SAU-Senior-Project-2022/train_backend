from pymongo import MongoClient, ASCENDING
from datetime import datetime
try:
    __database = MongoClient().train
except:
    pass
# def connect():
#     database = MongoClient().train

def getHistory(id: int) -> list:
   return [x for x in __database.history.find({'station_id': id})]

def getState(id: int) -> bool:
    return __database.history.find({'station_id': id}).sort('time', ASCENDING)[0]['state']

def getStation(id: int) -> dict:
    return __database.station.find_one({'station_id': id})

def setState(id: int, state: bool) -> bool:
    __database.history.insert({
        'station_id': id,
        'state': state,
        'time': datetime.utcnow()
    })
    return getState(id) == state
        

def setStation(id: int, lat: str, lon: str) -> bool:
    __database.history.insert({
        'station_id': id,
        'latitude': lat,
        'longitude': lon
    })
    database_station = getStation(id)
    if (database_station.get('station_id') != id):
        return False
    if (database_station.get('latitude') != lat):
        return False
    if (database_station.get('longitude') != lon):
        return False
    return True
    