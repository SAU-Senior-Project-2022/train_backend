import mariadb
from datetime import datetime
from sys import stderr, exit
import data
connection = None
db = None 
def connect(username: str, password: str, url: str="localhost", port: int=3306, database: str="train"):
    global db
    global connection
    try:
        connection = mariadb.connect(
            user=username,
            password=password,
            host=url
            port=port
            database=database
        )
    except mariadb.Error as e:
        print(f"Error connecting to MariaDB Platform: {e}", file=stderr)
        exit(2)
    db=connection.cursor()
    __check_database_create(database)

def check_tables(tableName, database_name):
    
    db.cursor.execute("SELECT count(*) FROM information_schema.TABLES WHERE (TABLE_SCHEMA = ?) AND (TABLE_NAME = ?)", (database_name, tableName))
    if (db.cursor.fetchone()[0] > 0):
        return True
    else:
        return False
def __check_database_create(database_name):
    if ((check_tables('history') != check_tables('station'))):
        if(check_tables('history')):
            __drop_table('history')
        else:
            __drop_table('station')
        create_database()

def __drop_table(table_name):
    db.cursor.execute("DROP TABLE ?", (table_name))
    connection.commit()
    return True

def create_database():
    db.execute("CREATE TABLE 'history' ('id' int(11) NOT NULL,'state' bit(1) NOT NULL,'date' datetime NOT NULL DEFAULT current_timestamp(), 'station_id' int(11) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")
    db.execute("CREATE TABLE `station` (`id` int(11) NOT NULL, `latitude` decimal(10,10) NOT NULL,`longitude` decimal(10,10) NOT NULL) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;")
    db.execute("ALTER TABLE `history` ADD PRIMARY KEY (`id`),ADD KEY `fk_history_station` (`station_id`);")
    db.execute("ALTER TABLE `station` ADD PRIMARY KEY (`id`); ALTER TABLE `history` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT; ALTER TABLE `station` MODIFY `id` int(11) NOT NULL AUTO_INCREMENT; ALTER TABLE `history` ADD CONSTRAINT `fk_history_station` FOREIGN KEY (`station_id`) REFERENCES `station` (`id`);")
    connection.commit()

def getHistory(id: int) -> list[data.history]:
    db.execute("SELECT id, state, date, station_id FROM history WHERE id=?", (id,))
    rows = db.fetchall()
    history_instances = []
    for row in rows:
        history_instances.push(data.history(row[0], row[1], row[2], row[3]))
    return history_instances
    
def getState(id: int) -> int:
    db.execute("SELECT state FROM history WHERE id=? ORDER BY date DESC LIMIT 1", (id,))
    row = db.fetchone()
    return row[0]

def getStation(id: int) -> data.station:
    db.execute("SELECT id, latitude, longitude FROM station WHERE id=?", (id,))
    row = db.fetchone()
    return data.station(row[0], row[1], row[2])

def setState(id: int, state: bool) -> dict:
    if (state == None):
        return {"error": f"Received a state of None"}
    db.execute("INSERT INTO history (state, station_id) VALUES (?, ?);", (id, state))
    connection.commit()
    return {"success": getHistory(id).id == id}

def insert_new_station(lat: float, lon: float):
    db.execute("INSERT INTO station (latitude, longitude) VALUES (?, ?);", (lat, lon))
    connection.commit()
    return {'station_id': db.lastrowid}