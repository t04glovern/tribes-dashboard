from pymongo import MongoClient
from datetime import datetime
import random


client = MongoClient('docker.nathanglover.com:27017')
db = client['tribes']
col = db.get_collection('tribes-data')

base_lon = 115.8528094
base_lat = -31.9540024


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
    return float(format(base_lon + random.uniform(0.0001, 0.001), '.8f'))


def random_lat():
    return float(format(base_lat + random.uniform(0.0001, 0.001), '.8f'))


# Remove all old entries
col.delete_many({})

# Add 100 random entries
for x in range(101, 110):
    data = {
        'timestamp': datetime.utcnow().isoformat(),
        'sensor_id': "NODE-" + str(x),
        'sensor_mac': random_mac(),
        'location_lon': random_lon(),
        'location_lat': random_lat(),
        'datestamp': datetime.utcnow().isoformat(),
        'altitude': random.uniform(20, 40),
        'velocity': random.uniform(0, 5),
        'GPSerror': random.choice([True, False]),
        'IMUerror': random.choice([True, False]),
        'rightdirection': random.choice([True, False]),
        'course': random.uniform(0, 5),
        'nstats': random.uniform(0, 5),
        'snr1': random.randint(-80, 80),
        'snr2': random.randint(-80, 80),
        'snr3': random.randint(-80, 80),
        'snr4': random.randint(-80, 80)
    }
    col.insert_one(data)
