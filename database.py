import mariadb
from datetime import datetime
from sys import stderr, exit
import data
import random

connection = None
db = None 
def connect(username: str, password: str, url: str="localhost", port: int=3306, database: str="train", fresh_migrate: bool=False):
    global db
    global connection
    try:
        connection = mariadb.connect(
            user=username,
            password=password,
            host=url,
            port=port,
            database=database
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}", file=stderr)
        exit(2)
    db=connection.cursor()
    if(fresh_migrate):
        __migrate_fresh(database)
    __check_database_create(database)

def __migrate_fresh(database_name):
    if(check_tables('history', database_name)):
        __drop_table('history')
    if(check_tables('station', database_name)):
        __drop_table('station')
    return True


def check_tables(tableName, database_name):
    
    db.execute("SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA = ?) AND (TABLE_NAME = ?)", (database_name, tableName))
    if (db.fetchone()[0] > 0):
        return True
    else:
        return False

def __check_database_create(database_name):
    if ((check_tables('history', database_name) != check_tables('station', database_name))):
        if(check_tables('history')):
            __drop_table('history')
        else:
            __drop_table('station')
        
    if (not check_tables('history', database_name) and not check_tables('station', database_name)):
        create_database()
    elif((check_tables('history', database_name) != check_tables('station', database_name))):
        print("Could not drop tables properly")
        exit(2)

def __drop_table(table_name):
    if table_name == 'history':
        db.execute("DROP TABLE history;")
    elif table_name == 'station':
        db.execute("DROP TABLE station;")
    connection.commit()
    return True

def create_database():
    # db.execute("CREATE TABLE `history` (`id` int(11) NOT NULL,`state` bit(1) NOT NULL, `date` datetime NOT NULL DEFAULT current_timestamp(), `station_id` int(11) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")
    # db.execute("CREATE TABLE `station` (`id` int(11) NOT NULL, `latitude` decimal(10,10) NOT NULL,`longitude` decimal(10,10) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")
    # db.execute("ALTER TABLE `history` ADD PRIMARY KEY (`id`); ALTER TABLE `station` ADD PRIMARY KEY (`id`); ALTER TABLE `history` ADD KEY `fk_history_station` (`station_id`);")
    # db.execute("ALTER TABLE `history` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT; ALTER TABLE `station` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT; ALTER TABLE `history` ADD CONSTRAINT `fk_history_station` FOREIGN KEY (`station_id`) REFERENCES `station` (`id`);")
    # connection.commit()
    db.execute("CREATE TABLE `history` (`id` int(11) NOT NULL,`state` tinyint(1) NOT NULL,`date` datetime NOT NULL DEFAULT current_timestamp(),`station_id` int(11) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")
    db.execute("CREATE TABLE `station` (`id` int(11) NOT NULL,`latitude` float(20,10) NOT NULL,`longitude` float(20,10) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")
    db.execute("ALTER TABLE `history` ADD PRIMARY KEY (`id`),ADD KEY `fk_history_station` (`station_id`);")
    db.execute("ALTER TABLE `station` ADD PRIMARY KEY (`id`);")
    db.execute("ALTER TABLE `history` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;")
    db.execute("ALTER TABLE `station` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;")
    db.execute("ALTER TABLE `history` ADD CONSTRAINT `fk_history_station` FOREIGN KEY (`station_id`) REFERENCES `station` (`id`);")
    connection.commit()

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
    db.execute("INSERT INTO history (state, station_id) VALUES (?, ?);", (state, id))
    connection.commit()
    return {"success": int(getState(id).station_id) == int(id)}

def insert_new_station(lat: float, lon: float):
    db.execute("INSERT INTO station (latitude, longitude) VALUES (?, ?);", (float(lat), float(lon)))
    connection.commit()
    return {'station_id': db.lastrowid}