-- SQLite
CREATE TABLE station (id INTEGER PRIMARY KEY NOT NULL, title TEXT, latitude DECIMAL(30,16) NOT NULL, longitude DECIMAL(30,16) NOT NULL);
CREATE TABLE history (id INTEGER PRIMARY KEY, state tinyint(1) NOT NULL, date TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')), station_id INTEGER, FOREIGN KEY (station_id) REFERENCES station(id));
INSERT INTO station (latitude, longitude, title) VALUES (35.0790872, -85.03379881, 'Edgemon Lee');
INSERT INTO station (latitude, longitude, title) VALUES (35.05329595, -85.04855633, 'Apison Pike');
INSERT INTO station (latitude, longitude, title) VALUES (35.07087755, -85.06399512, 'Main Street');
INSERT INTO station (latitude, longitude, title) VALUES (35.09772104, -85.00740051, 'South Lee');
INSERT INTO history (state, station_id) VALUES (1, 1);
INSERT INTO history (state, station_id) VALUES (0, 2);
INSERT INTO history (state, station_id) VALUES (1, 3);
INSERT INTO history (state, station_id) VALUES (0, 4);