import unittest
from server import app
import database
#import server
import requests
#from random_word import RandomWords
import random
#seed database
station_ids = []
def seed_database():
    for i in range(22):
        station_id = database.insert_new_station(123123,12341234)
        print(station_id)
        station_ids.append(station_id)
    for i in station_ids:
        for j in range(22):
            database.setState(i.get('station_id'), int(random.getrandbits(1)))


# Test    
# Failing tests here
class TestServerMethods(unittest.TestCase):
    def test_my_life(this):
        this.assertTrue("I do not have a life")
    def test_state_get(this):
        #get last state created in first station
        #print(database.db.history.find({'station_id': station_ids[0]}).sort('time', pymongo.DESCENDING))
        print("here")
        print(database.db.history.find({'station_id': station_ids[0]}).sort('time', pymongo.DESCENDING).limit(1)[0].get('station_id'))
        with server.app.app_context():
            print('inside')
            print(state.get(None,station_ids[0]).get('station_id'))
            #this.assertEquals(database.db.history.find({'station_id': station_ids[0]}).sort('time', pymongo.DESCENDING).limit(1)[0].get('station_id'), State.get(None,station_ids[0]).get('station_id'))

if __name__ == "__main__":
    database.connect(username="test", password="conn123", url="0.0.0.0", database="train_test", fresh_migrate=True)

    # Create new database


    # Connect
    #database.db = database.db.train_test
    seed_database()
    #unittest.main()
    #test_seed()
    unittest.main()
    
    # Destroy database

