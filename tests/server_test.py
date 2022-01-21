import unittest
import requests
URL = "http://localhost:5000"

station_ids = []
def get_locations():
    data = requests.get(URL + "/location").json()
    for entry in data:
        station_ids.append(entry["id"])
class TestServerMethods(unittest.TestCase):
    def test_my_life(this):
        this.assertTrue("I do not have a life")
    def test_get_locations(this):
        data = requests.get(URL + "/location").json()
        for entry in data:
            this.assertEqual(entry.get("error_message"), "")
            this.assertEqual(entry.get("error_state"), False)
        this.assertEqual(len(data), len(station_ids))
    def test_get_location_by_id(this):
        for id in station_ids:
            data = requests.get(URL + "/location/" + str(id)).json()
            this.assertEqual(data.get("error_message"), "")
            this.assertEqual(data.get("error_state"), False)
            this.assertEqual(data.get("id"), id)
            this.assertEqual(data.get("latitude"), 123123.0)
            this.assertEqual(data.get("longitude"), 12341234.0)
    def test_get_state(this):
        for id in station_ids:
            data = requests.get(URL + "/state/" + str(id)).json()
            # for entry in data:
            this.assertEqual(data.get("error_message"), "")
            this.assertEqual(data.get("error_state"), False)
            this.assertEqual(data.get("station_id"), id)
            # this.assertEqual(data.get("id"), id)     
    def test_post_state(this):
        data = requests.post(URL + "/state/"+str(station_ids[0]), json={"station_id": station_ids[0], "state": 1}).json()
        data_get_state = requests.get(URL + "/state/" + str(station_ids[0])).json()
        this.assertTrue(data.get("success"))
        this.assertEqual(data_get_state.get("error_message"), "")
        this.assertEqual(data_get_state.get("error_state"), False)
        this.assertEqual(data_get_state.get("station_id"), station_ids[0])
        this.assertEqual(data_get_state.get("state"), 1)
    def test_post_location(this):
        data = requests.post(URL + "/location/new", json={"latitude": 123123.0, "longitude": 12341234.0}).json()
        # print(data.get("station)
        this.assertFalse(data.get("station_id") == None)
        data_get_location = requests.get(URL + "/location/" + str(data.get("station_id"))).json()
        this.assertEqual(data_get_location.get("error_message"), "")
        this.assertEqual(data_get_location.get("error_state"), False)
        this.assertEqual(data_get_location.get("latitude"), 123123.0)
        this.assertEqual(data_get_location.get("longitude"), 12341234.0)

if __name__ == "__main__":
    get_locations()
    unittest.main()

