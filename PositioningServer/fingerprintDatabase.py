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

class Fingerprints(db.Entity):
    id = PrimaryKey(int, auto=True)
    advertised_device = Required(str, 255)
    rssi = Required(int)
    date = Required(datetime.datetime)


db.bind(provider='mysql', **db_config)
db.generate_mapping(create_tables=True)