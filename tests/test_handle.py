import requests
URL = "http://train.jpeckham.com:5000"

station_ids = []
def get_locations():
    data = requests.get(URL + "/location").json()
    for entry in data:
        print(entry["id"])
        station_ids.append(entry["id"])
def test_get_locations():
    while(True):
        for station in station_ids:
            data = requests.get(URL + "/location/" + str(station)).json()
            print(data.get("id"))

if __name__ == "__main__":
    get_locations()
    test_get_locations()