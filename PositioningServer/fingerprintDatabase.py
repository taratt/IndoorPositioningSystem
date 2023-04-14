from dotenv import load_dotenv, find_dotenv
from os import getenv
import datetime
from pony.orm import *


load_dotenv(find_dotenv())

db_config = {
    "host": getenv("DB_HOST"),
    "user": getenv("DB_USER"),
    "passwd": getenv("DB_PASS"),
    "db": getenv("DB_NAME"),
}

db = Database()

class Advertisement(db.Entity):
    id = PrimaryKey(int, auto=True)
    scan_number = Required(int)
    advertised_device = Required('Beacon')
    advertised_channel =Required(int)
    rssi = Required(int)
    date = Required(datetime.datetime)
    location = Required(str, 255)

class Beacon(db.Entity):
    beacon_name = PrimaryKey(str, 255)
    mac_address = Required(str, 255)
    level = Required(int)
    fingerprints = Set('Advertisement')

class Fingerprint(db.Entity):
    scan_number = PrimaryKey(int)
    date = Required(datetime.datetime)
    beacon1 = Optional(int, default = 0)
    channel1 = Optional(int, default = 0)
    beacon2 = Optional(int, default = 0)
    channel2 = Optional(int, default = 0)
    beacon3 = Optional(int, default = 0)
    channel3 = Optional(int, default = 0)
    beacon4 = Optional(int, default = 0)
    channel4 = Optional(int, default = 0)
    beacon5 = Optional(int, default = 0)
    channel5 = Optional(int, default = 0)
    beacon6 = Optional(int, default = 0)
    channel6 = Optional(int, default = 0)
    beacon7 = Optional(int, default = 0)
    channel7 = Optional(int, default = 0)
    beacon8 = Optional(int, default = 0)
    channel8 = Optional(int, default = 0)
    beacon9 = Optional(int, default = 0)
    channel9 = Optional(int, default = 0)
    beacon10 = Optional(int, default = 0)
    channel10 = Optional(int, default = 0)
    beacon11 = Optional(int, default = 0)
    channel11 = Optional(int, default = 0)
    beacon12 = Optional(int, default = 0)
    channel12 = Optional(int, default = 0)
    beacon13 = Optional(int, default = 0)
    channel13 = Optional(int, default = 0)
    beacon14 = Optional(int, default = 0)
    channel14 = Optional(int, default = 0)
    beacon15 = Optional(int, default = 0)
    channel15 = Optional(int, default = 0)
    beacon16 = Optional(int, default = 0)
    channel16 = Optional(int, default = 0)
    beacon17 = Optional(int, default = 0)
    channel17 = Optional(int, default = 0)
    beacon18 = Optional(int, default = 0)
    channel18 = Optional(int, default = 0)
    beacon19 = Optional(int, default = 0)
    channel19 = Optional(int, default = 0)
    beacon20 = Optional(int, default = 0)
    channel20 = Optional(int, default = 0)
    # beacon21 = int
    # channel21 = int
    # beacon22 = int
    # channel22 = int
    location = Required(str, 255)

db.bind(provider='mysql', **db_config)
db.generate_mapping(create_tables=True)

with db_session:
    if Beacon.select().first() is None:
        Beacon(beacon_name='beacon1', mac_address= '7c:9e:bd:fb:da:e6', level = 5)
        Beacon(beacon_name='beacon2', mac_address='7c:9e:bd:fb:d8:da', level = 5)
        Beacon(beacon_name='beacon3', mac_address='7c:9e:bd:fb:d9:ee', level = 5)
        Beacon(beacon_name='beacon4', mac_address='7c:9e:bd:fb:d8:42', level = 5)
        Beacon(beacon_name='beacon5', mac_address='7c:9e:bd:fb:d9:5e', level = 5)
        Beacon(beacon_name='beacon6', mac_address='7c:9e:bd:fb:d8:e2', level = 5)
        Beacon(beacon_name='beacon7', mac_address='7c:9e:bd:fb:dc:1e', level = 5)
        Beacon(beacon_name='beacon8', mac_address='7c:9e:bd:fb:d9:9a', level = 5)
        Beacon(beacon_name='beacon9', mac_address='7c:9e:bd:fb:d8:4a', level = 5)
        Beacon(beacon_name='beacon10', mac_address='7c:9e:bd:fb:da:12', level = 5)
        Beacon(beacon_name='beacon11', mac_address='7c:9e:bd:fb:da:e6', level = 2)
        Beacon(beacon_name='beacon12', mac_address='7c:9e:bd:fb:d8:da', level = 2)
        Beacon(beacon_name='beacon13', mac_address='7c:9e:bd:fb:d9:ee', level = 2)
        Beacon(beacon_name='beacon14', mac_address='7c:9e:bd:fb:d8:42', level = 2)
        Beacon(beacon_name='beacon15', mac_address='7c:9e:bd:fb:d9:5e', level = 2)
        Beacon(beacon_name='beacon16', mac_address='7c:9e:bd:fb:d8:e2', level = 2)
        Beacon(beacon_name='beacon17', mac_address='7c:9e:bd:fb:dc:1e', level = 2)
        Beacon(beacon_name='beacon18', mac_address='7c:9e:bd:fb:d9:9a', level = 2)
        Beacon(beacon_name='beacon19', mac_address='7c:9e:bd:fb:d8:4a', level = 2)
        Beacon(beacon_name='beacon20', mac_address='7c:9e:bd:fb:da:12', level = 2)

        # Beacon(beacon_name='beacon21', mac_address='7c:9e:bd:fb:d8:c6', level=5)
        # Beacon(beacon_name='beacon22', mac_address='7c:9e:bd:fb:d8:c6', level=2)






