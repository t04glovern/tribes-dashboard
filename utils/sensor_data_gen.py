from pymongo import MongoClient
from datetime import datetime
import random


client = MongoClient('docker.nathanglover.com:27017')
db = client['tribes']
col = db.get_collection('tribes-data')

base_lon = 115.8614643
base_lat = -31.9744023


def random_mac():
    return "%02x:%02x:%02x:%02x:%02x:%02x" % (
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255),
        random.randint(0, 255)
    )


def random_lon():
    return float(format(base_lon + random.uniform(-0.002, 0.002), '.4f'))


def random_lat():
    return float(format(base_lat + random.uniform(-0.002, 0.002), '.4f'))


# Remove all old entries
col.delete_many({})

# Add 100 random entries
for x in range(101, 110):
    data = {
        'timestamp': datetime.utcnow().isoformat(),
        'sensor_id': "NODE-" + str(x),
        'sensor_mac': random_mac(),
        'location_lon': random_lon(),
        'location_lat': random_lat()
    }
    col.insert_one(data)
