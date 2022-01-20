import datetime
import json
class history(object):
    id            : int
    state         : bool
    date          : datetime.datetime
    station_id    : int
    error_state   : bool
    error_message : str
    def __init__(self, id: int, state: bool, date: datetime.datetime, station_id : int, error_message: str = ""):
        self.id = id
        self.state = state
        self.date = date
        self.station_id = station_id
        self.error_state = False if error_message == "" else True
        self.error_message = error_message
    
    class HistoryEncoder(json.JSONEncoder):
        def default(self, o):
            if (o.error_state):
                return { "error": o.error_message }
            else:
                o.date = {"year":o.date.year, "month":o.date.month, "day":o.date.day, "hour":o.date.hour, "minute":o.date.minute, "second":o.date.second}
                return o.__dict__

class station(object):
    id : int
    latitude : float
    longitude : float
    error_state   : bool
    error_message : str
    def __init__(self, id: int, latitude: float, longitude: float, error_message: str = ""):
        self.id = id
        self.latitude = latitude
        self.longitude = longitude
        self.error_state = False if error_message == "" else True
        self.error_message = error_message
    class StationEncoder(json.JSONEncoder):
        def default(self, o):
            return {"error": o.error_message} if (o.error_state) else o.__dict__
