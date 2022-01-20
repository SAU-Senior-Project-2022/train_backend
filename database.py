import mariadb
from sys import stderr, exit
import data
import random

connection = None
db = None 

def connect(username: str, password: str, 
    url: str="localhost", port: int=3306, 
    database: str="train", fresh_migrate: bool=False):
    """Connects to database with specified arguments.

    Args:
        username (str): Username to connect with.
        password (str): Password to connect with.
        url (str, optional): URL/IP of database. Defaults to "localhost".
        port (int, optional): Port database is run on. Defaults to 3306.
        database (str, optional): Name of the database to connect to. Defaults to "train".
        fresh_migrate (bool, optional): If True, deletes database and creates fresh empty database. Defaults to False.
    """
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
        print(f"(database.py:connect) Error connecting to MariaDB Platform: {e}", file=stderr)
        exit(2)
    db=connection.cursor()
    if(fresh_migrate):
        __migrate_fresh(database)
    __check_database_create(database)

def __migrate_fresh(database_name: str) -> bool:
    """Creates new empty database

    Args:
        database_name (str): Name of the database to use

    Returns:
        bool: True
    """
    if(check_tables('history', database_name)):
        __drop_table('history')
    if(check_tables('station', database_name)):
        __drop_table('station')
    create_database()
    return True


def check_tables(tableName: str, database_name: str) -> bool:
    """Checks if `tableName` exists in `database_name`

    Args:
        tableName (str): Name of table to check for
        database_name (str): Name of database to check in

    Returns:
        bool: If table exists, error is False
    """
    try:
        db.execute("SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA = ?) AND (TABLE_NAME = ?)", (database_name, tableName))
    except:
        print("(database.py:check_tables) SELECT failed")
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
    if ((check_tables('history', database_name) != check_tables('station', database_name))):
        if(check_tables('history')):
            __drop_table('history')
        else:
            __drop_table('station')
        
    if (not check_tables('history', database_name) and not check_tables('station', database_name)):
        create_database()
    elif((check_tables('history', database_name) != check_tables('station', database_name))):
        print("(database.py:__check_database_create) Could not drop tables properly")
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
        print(f"(database.py:__drop_table) Failed to drop table {table_name}")
        exit(2)
    return True

def create_database() -> bool:
    """Creates database for project

    Returns:
        bool: True
    """
    try:
        db.execute("CREATE TABLE `history` (`id` int(11) NOT NULL,`state` tinyint(1) NOT NULL,`date` datetime NOT NULL DEFAULT current_timestamp(),`station_id` int(11) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")
        db.execute("CREATE TABLE `station` (`id` int(11) NOT NULL,`latitude` float(20,10) NOT NULL,`longitude` float(20,10) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")
        db.execute("ALTER TABLE `history` ADD PRIMARY KEY (`id`),ADD KEY `fk_history_station` (`station_id`);")
        db.execute("ALTER TABLE `station` ADD PRIMARY KEY (`id`);")
        db.execute("ALTER TABLE `history` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;")
        db.execute("ALTER TABLE `station` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;")
        db.execute("ALTER TABLE `history` ADD CONSTRAINT `fk_history_station` FOREIGN KEY (`station_id`) REFERENCES `station` (`id`);")
        connection.commit()
    except:
        print("(database.py:create_database) Failed to create database from scratch")
        exit(2)
    return True

def seed_database() -> bool:
    """Seeds database with some test data

    Returns:
        bool: True
    """
    station_ids = []
    for i in range(22):
        station_id = insert_new_station(123123,12341234)
        print(station_id)
        station_ids.append(station_id)
    for i in station_ids:
        for j in range(22):
            setState(i, bool(random.getrandbits(1)))
    return True

def getHistory(id: int) -> list[data.history]:
    """Gets all history of a station

    Args:
        id (int): id to query with

    Returns:
        list[data.history]: List of history
    """
    try:
        db.execute("SELECT id, state, date, station_id FROM history WHERE station_id=? ORDER BY date DESC", (id,))
    except:
        return [data.history(error_message="There was an error in the database")]
    rows = db.fetchall()
    history_instances = []
    for row in rows:
        history_instances.append(data.history(row[0], row[1], row[2], row[3]))
    return history_instances
    
def getState(id: int) -> data.history:
    """Gets the state of a station

    Args:
        id (int): Station id

    Returns:
        data.history: latest station history
    """    
    try:
        db.execute("SELECT id, state, date, station_id FROM history WHERE station_id=? ORDER BY date DESC LIMIT 1", (id,))
    except:
        return [data.history(error_message="There was an error in the database")]
    column = db.fetchone()
    return data.history(column[0], column[1], column[2], column[3])

def getStation(id: int) -> data.station:
    """Gets station info

    Args:
        id (int): Station id

    Returns:
        data.station: Station info
    """
    try:
        db.execute("SELECT id, latitude, longitude FROM station WHERE id=?;", (id,))
    except:
        return [data.history(error_message="There was an error in the database")]
    row = db.fetchone()
    return data.station(row[0], row[1], row[2])

def setState(id: int, state: int) -> dict:
    """Sets the state of a station

    Args:
        id (int): Station id
        state (int): new state

    Returns:
        dict: "success" or "error"
    """
    if (state == None):
        return {"error": f"Received a state of None"}
    try:
        db.execute("INSERT INTO history (state, station_id) VALUES (?, ?);", (state, id))
    except:
        return [{"error": "There was an error in the database"}]
    connection.commit()
    return {"success": int(getState(id).station_id) == int(id)}

def insert_new_station(lat: float, lon: float) -> dict:
    """Inserts new

    Args:
        lat (float): Latitude
        lon (float): Longitude

    Returns:
        dict: {'station_id': id}
    """
    try:
        db.execute("INSERT INTO station (latitude, longitude) VALUES (?, ?);", (float(lat), float(lon)))
    except:
        return [{"error": "There was an error in the database"}]
    connection.commit()
    return {'station_id': db.lastrowid}