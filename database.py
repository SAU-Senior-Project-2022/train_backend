from pymongo import MongoClient, DESCENDING, ASCENDING
from pymongo.errors import ConnectionFailure
from datetime import datetime
from sys import stderr
connection = None
db = None

def connect(url: str="mongo", port: int=27017, database: str="train"):
    # Connect to database
    global connection, db
    connection = MongoClient(url, port=port)

    # Check connection
    try:
        connection.admin.command('ping')
    except ConnectionFailure:
        print("Server not available")
        exit(1)
    if (database == "train"):
        db = connection.train
        if ("history" not in db.list_collection_names()):
            db.create_collection("history")
        if ("station" not in db.list_collection_names()):
            db.create_collection("station")
    elif (database == "train_test"):
        db = connection.train_test
    else:
        print(f"Database: {database} is not a valid choice, please choose \"train\" or \"train_test\"", file=stderr)
        exit(2)

def getHistory(id: int) -> list[dict]:
    """Gets the history of `id` from the database

    Args:
        id (int): Id of the station

    Returns:
        list[dict]: Dict objects containing time and state of `id` location
    """
    if (db.history.count_documents({'station_id': id}) == 0):
        return [{"error": f"{id} is not a valid id"}]
    return [x for x in db.history.find({'station_id': id})]

def getState(id: int) -> dict:
    """Gets the history of `id` from the database

    Args:
        id (int): Id of the station

    Returns:
        bool: `True` means there is a blockage of the railroad,
        while `False` means the crossing appears to be clear
    """
    print(str(db.history.find({'station_id': id}).sort('time', DESCENDING).limit(1)[0]))
    if (db.history.count_documents({'station_id': id}) == 0):
        return {"error": f"{id} is not a valid id"}
    return db.history.find({'station_id': id}).sort('time', DESCENDING).limit(1)[0]

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
    if (db.station.count_documents({'station_id': id}) == 0):
        return {"error": f"{id} is not a valid id"}
    return db.station.find_one({'station_id': id})

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
    db.history.insert_one(data)
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
    if (db.station.count_documents({}) == 0):
        largest_station_id = -1 # Will be incremented in a few lines
    else:
        largest_station_id = db.station.find().sort('station_id', DESCENDING)[0].get('station_id')
    new_station_id = largest_station_id + 1
    data = {
        'station_id': new_station_id,
        'latitude': lat,
        'longitude': lon
    }
    #db.station.insert_one(data)
    # insert_id = db.station.insert_one(data).inserted_id
    # print("TEST!")
    # print(insert_id)
    if (not db.station.insert_one(data).inserted_id):
        return {"error": "Could not create new station"}
    return {'station_id':new_station_id}
    