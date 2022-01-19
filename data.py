import datetime
import json
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
    
    class HistoryEncoder(json.JSONEncoder):
        def default(self, o):
            print(o)
            #o.date = [o.date.year, o.date.month, o.date.day, o.date.hour, o.date.minute, o.date.second]
            o.date = {"year":o.date.year, "month":o.date.month, "day":o.date.day, "hour":o.date.hour, "minute":o.date.minute, "second":o.date.second}
            return o.__dict__

class station(object):
    id : int
    latitude : float
    longitude : float
    def __init__(self, id: int, latitude: float, longitude: float):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
    class StationEncoder(json.JSONEncoder):
        def default(self, o):
            return o.__dict__

# class settings(object):
#     name : str
#     username : str
#     password : str 
#     url : str
#     port : int

#     def __init__(self, username : str, password : str, url : str="0.0.0.0", port : int=3306, name : str="train"):
#         self.name = name
#         self.username = username
#         self.password = password
#         self.url = url
#         self.port = port