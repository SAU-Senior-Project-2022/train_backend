from pymongo import MongoClient, DESCENDING, ASCENDING
from pymongo.errors import ConnectionFailure
from datetime import datetime

# Connect to database
__database = MongoClient("0.0.0.0")

# Check connection
try:
    __database.admin.command('ping')
except ConnectionFailure:
    print("Server not available")
    exit(1)

# If connected, redefine __database as our database, not the connection
__database = __database.train

# Make sure collections exist
if ("history" not in __database.list_collection_names()):
    __database.create_collection("history")
if ("station" not in __database.list_collection_names()):
    __database.create_collection("station")

def getHistory(id: int) -> list[dict]:
    """Gets the history of `id` from the database

    Args:
        id (int): Id of the station

    Returns:
        list[dict]: Dict objects containing time and state of `id` location
    """
    if (__database.history.count_documents({'station_id': id}) == 0):
        return [{"error": f"{id} is not a valid id"}]
    return [x for x in __database.history.find({'station_id': id})]

def getState(id: int) -> dict:
    """Gets the history of `id` from the database

    Args:
        id (int): Id of the station

    Returns:
        bool: `True` means there is a blockage of the railroad,
        while `False` means the crossing appears to be clear
    """
    if (__database.history.count_documents({'station_id': id}) == 0):
        return {"error": f"{id} is not a valid id"}
    return __database.history.find({'station_id': id}).sort('time', DESCENDING).limit(1)[0]

def getStation(id: int) -> dict:
    """Gets the station's physical location from the `id`

    Args:
        id (int): Id of the station

    Returns:
        dict: {
            'station_id': `id`, 
            'latitude': <physical_latitude>, 
            'longitude': <physical_longitude>
        }
    """
    if (__database.station.count_documents({'station_id': id}) == 0):
        return {"error": f"{id} is not a valid id"}
    return __database.station.find_one({'station_id': id})

def setState(id: int, state: bool) -> dict:
    """Sets the state of the station

    Args:
        id (int): Id of the station
        state (bool): `True` means there is a blockage, while `False` means it appears to be clear`

    Returns:
        bool: state of update
    """
    if (state == None):
        return {"error": f"Received a state of None"}
    data = {
        'station_id': id,
        'state': state,
        'time': datetime.utcnow()
    }
    __database.history.insert_one(data)
    if (getState(id).get('error') != None):
        return {"error": f"failed to insert new state of {state} for station {id}"}
    return {"success":getState(id) == data}
        
def insert_new_station(lat: str, lon: str) -> dict:
    """Inserts a new station

    Args:
        lat (str): Physical latitude
        lon (str): Physical longitude

    Returns:
        int: The id of the station if successfull, otherwise returns `None`
    """
    if (__database.station.count_documents({}) == 0):
        largest_station_id = -1 # Will be incremented in a few lines
    else:
        largest_station_id = __database.station.find().sort('station_id', ASCENDING)[0].get('station_id')
    new_station_id = largest_station_id + 1
    data = {
        'station_id': new_station_id,
        'latitude': lat,
        'longitude': lon
    }
    __database.station.insert_one(data)
    if (data != getStation(new_station_id)):
        return {"error": "Could not create new station"}
    return {'station_id':new_station_id}
    