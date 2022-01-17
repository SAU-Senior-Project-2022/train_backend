import datetime
class history(object):
    id : int
    state : bool
    date : datetime.datetime
    station_id : int
    def __init__(self, id: int, state: bool, date: datetime.datetime, station_id : int):
        self.id = id
        self.state = state
        self.date = date
        self.station_id = station_id

class station(object):
    id : int
    latitude : float
    longitude : float
    def __init__(self, id: int, latitude: float, longitude: float):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude

class settings(object):
    name : str
    username : str
    password : str 
    url : str
    port : int

    def __init__(self, username : str, password : str, url : str="0.0.0.0", port : int=3306, name : str="train"):
        self.name = name
        self.username = username
        self.password = password
        self.url = url
        self.port = port