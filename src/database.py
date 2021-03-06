# import mariadb
import sqlite3
import datetime
from sys import stderr, exit
import data
import random

connection = None
db = None 
__uname = None
__pass = None
__url = None
__port = None
__dbname = None

def connect(database:str, fresh_migrate:bool=False) -> bool:
    """Connects to database with specified arguments.

    Args:
        username (str): Username to connect with.
        password (str): Password to connect with.
        url (str, optional): URL/IP of database. Defaults to "localhost".
        port (int, optional): Port database is run on. Defaults to 3306.
        database (str, optional): Name of the database to connect to. Defaults to "train".
        fresh_migrate (bool, optional): If True, deletes database and creates fresh empty database. Defaults to False.
    """
    global db, connection, __dbname
    # global db, connection, __uname, __pass, __url, __port, __dbname
    # __uname = username
    # __pass = password
    # __url = url
    # __port = port
    __dbname = database
    try:
        connection = sqlite3.connect(database,check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES)
    except sqlite3.Error as e:
        print(f"(database.py:connect) Error connecting to Sqlite Platform: {e}", file=stderr)
        exit(2)
    db=connection.cursor()
    if(fresh_migrate):
        __drop_tables(database)
    __check_database_create(database)
    #connection.close()
    __auto_connect()

def __auto_connect():
    # print("__auto_connect")
    # global connection, db
    try:
        global db, connection
        connection = sqlite3.connect(__dbname,check_same_thread=False, detect_types=sqlite3.PARSE_DECLTYPES)
        db=connection.cursor()
    except sqlite3.Error as e:
        print(f"(database.py:connect) Error connecting to MariaDB Platform: {e}", file=stderr)
        exit(2)
    return True

def __auto_disconnect():
    global db, connection
    db.close()
    connection.close()
    db = None
    connection = None

def __drop_tables(database_name: str) -> bool:
    """Creates new empty database

    Args:
        database_name (str): Name of the database to use

    Returns:
        bool: True
    """
    if(__check_table('history', database_name)):
        __drop_table('history')
    if(__check_table('station', database_name)):
        __drop_table('station')
    return True


def __check_table(tableName: str, database_name: str) -> bool:
    """Checks if `tableName` exists in `database_name`

    Args:
        tableName (str): Name of table to check for
        database_name (str): Name of database to check in

    Returns:
        bool: If table exists, error is False
    """
    try:
        db.execute("SELECT count(*) FROM sqlite_master WHERE (type='table') AND (name = ?)", (tableName,))
    except sqlite3.Error as e:
        print(f"(database.py:__check_table) SELECT failed {e}", file=stderr)
        exit(2)
    if (db.fetchone()[0] > 0):
        return True
    else:
        return False

def __check_database_create(database_name: str) -> bool:
    """Checks if database is complient with 
    implementation, and will correct it if it is not.

    Args:
        database_name (str): Name of database to use
    """
    if(not __check_table('station', database_name)): # TODO ENFORCE ORDER
        __create_table_station()

    if(not __check_table('history', database_name)):
        __create_table_history()
        
    if((not __check_table('history', database_name)) or (not __check_table('station', database_name))):
        print("(database.py:__check_database_create) Could not drop tables properly", file=stderr)
        exit(2)
    return True

def __drop_table(table_name: str) -> bool:
    """Drops table, must be valid table.

    Args:
        table_name (str): Name of table to use

    Returns:
        bool: True
    """
    try:
        if (table_name in ['history', 'station']):
            db.execute(f"DROP TABLE {table_name};")
        connection.commit()
    except:
        print(f"(database.py:__drop_table) Failed to drop table {table_name}", file=stderr)
        exit(2)
    return True

def create_database() -> bool:
    """Creates database for project

    Returns:
        bool: True
    """
    __create_table_station()
    __create_table_history() ## TODO ENFORCE ORDER
    return True

def __create_table_station():
    try:
        #CREATE TABLE [IF NOT EXISTS] [schema_name].table_name (column_1 data_type PRIMARY KEY,column_2 data_type NOT NULL,column_3 data_type DEFAULT 0,table_constraints) [WITHOUT ROWID];
        db.execute("CREATE TABLE station (id INTEGER PRIMARY KEY NOT NULL, title TEXT, latitude DECIMAL(30,16) NOT NULL, longitude DECIMAL(30,16) NOT NULL);")
        #db.execute("ALTER TABLE `station` ADD PRIMARY KEY (`id`);")
        #db.execute("ALTER TABLE `station` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;")
        connection.commit()
    except sqlite3.Error as e:
        print(f"(database.py:__create_table_station) Failed to create database from scratch {e}", file=stderr)
        exit(2)
    return True

def __create_table_history():
    try:
        db.execute("CREATE TABLE history (id INTEGER PRIMARY KEY, state tinyint(1) NOT NULL, date TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')), station_id INTEGER, FOREIGN KEY (station_id) REFERENCES station(id));")
        # db.execute("ALTER TABLE `history` ADD PRIMARY KEY (`id`),ADD KEY `fk_history_station` (`station_id`);")
        # db.execute("ALTER TABLE `history` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;")
        # db.execute("ALTER TABLE `history` ADD CONSTRAINT `fk_history_station` FOREIGN KEY (`station_id`) REFERENCES `station` (`id`);")
        connection.commit()
    except sqlite3.Error as e:
        print(f"(database.py:__create_table_history) Failed to create database from scratch {e}", file=stderr)
        exit(2)
    return True

# def seed_database() -> bool:
#     """Seeds database with some test data

#     Returns:
#         bool: True
#     """
#     station_ids = []
#     for i in range(24):
#         station_id = insert_new_station(123123,12341234)
#         print("Station ID:",station_id)
#         station_ids.append(station_id.get("station_id"))
#     for i in station_ids:
#         for _ in range(23):
#             setState(i, int(random.getrandbits(1)))
#     return True

def getHistory(id: int) -> list[data.history]:
    """Gets all history of a station

    Args:
        id (int): id to query with

    Returns:
        list[data.history]: List of history
    """
    __auto_connect()
    #print("getHistory")
    try:
        db.execute("SELECT id, state, date, station_id FROM history WHERE station_id=? ORDER BY date DESC", (id,))
    except sqlite3.Error as e:
        print("e",e, file=stderr)
        return [data.history(error_message="There was an error in the database")]
    rows = db.fetchall()
    history_instances = []
    for row in rows:
        history_instances.append(data.history(row[0], row[1], row[2], row[3]))
    __auto_disconnect()
    return history_instances
    
def getState(id: int) -> data.history:
    """Gets the state of a station

    Args:
        id (int): Station id

    Returns:
        data.history: latest station history
    """ 
    __auto_connect()  
    #print("getState") 
    try:
        db.execute('SELECT id, state, date, station_id FROM history WHERE station_id=? ORDER BY date DESC LIMIT 1', (id,))
    except:
        return data.history(error_message="There was an error in the database")
    row = db.fetchone()
    # db.close()
    # connection.close()
    if (row == None):
        return data.history(error_message="State not found")
    __auto_disconnect()
    print(type(row[2]))
    return data.history(row[0], row[1], row[2], row[3])

def getStation(id: int) -> data.station:
    """Gets station info

    Args:
        id (int): Station id

    Returns:
        data.station: Station info
    """
    __auto_connect()
    #print("getStation")
    try:
        print("Before query")
        db.execute("SELECT id, latitude, longitude, title FROM station WHERE id=?;", (id,))
        print("After query")
    except sqlite3.Error as e:
        print(e)
        return [data.history(error_message="There was an error in the database")]
    row = db.fetchone()
    __auto_disconnect()
    # db.close()
    # connection.close()
    if (row == None):
        return data.station(error_message="Station not found")
    return data.station(row[0], row[1], row[2], row[3])

def setState(id: int, state: int) -> dict:
    """Sets the state of a station

    Args:
        id (int): Station id
        state (int): new state

    Returns:
        dict: "success" or "error"
    """
    __auto_connect()
    #print("setState")
    if (state == None):
        return {"error": f"Received a state of None"}
    try:
        db.execute("INSERT INTO history (state, station_id) VALUES (?, ?);", (state, id))
        connection.commit()
        __auto_disconnect()
        # db.close()
        # connection.close()
    except:
        return [{"error": "There was an error in the database"}]
    return {"success": int(getState(id).station_id) == int(id)}

def insert_new_station(lat: float, lon: float, title: str="no title") -> dict:
    """Inserts new station into database

    Args:
        lat (float): Latitude
        lon (float): Longitude

    Returns:
        dict: {'station_id': id}
    """
    __auto_connect()
    #print("insert_new_station")
    try:
        db.execute("INSERT INTO station (latitude, longitude, title) VALUES (?, ?, ?);", (float(lat), float(lon), title))
        connection.commit()
        # db.close()
        # connection.close()
    except sqlite3.Error as e:
        print(f"(database.py:connect) Error connecting to MariaDB Platform: {e}", file=stderr)
        return [{"error": "There was an error in the database"}]
    new_station_id = db.lastrowid
    __auto_disconnect()
    setState(new_station_id, 0)
    return {'station_id': new_station_id}

def getStationList() -> list[data.station]:
    """Gets list of all stations

    Returns:
        list[data.station]: List of stations
    """
    __auto_connect()
    print("getStationList")
    try:
        db.execute("SELECT id, latitude, longitude, title FROM station;")
    except sqlite3.Error as e:
        print("e",e, file=stderr)
        return [{"error": "There was an error in the database"}]
    rows = db.fetchall()
    __auto_disconnect()
    # db.close()
    # connection.close()
    if (rows == None):
        return [{"error": "No Stations found"}]
    else:
        return_array = []
        for row in rows:
            return_array.append(data.station(row[0], row[1], row[2], row[3]))
        return return_array