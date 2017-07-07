from flask import Flask, render_template, request, redirect, session, url_for
from functools import wraps
from hashlib import sha256
import json
import requests
import time

import secret

## Flask_MongoDB imports
from mongo import mongo

## Flask GoogleMaps
from flask_googlemaps import GoogleMaps, Map

## Flask_REST API imports
from flask_restful import Api
from api.resources.data import Data

'''
Init
'''
app = Flask(__name__)

# set the secret key. keep this really secret:
app.secret_key = secret.secret_key

# Load app configs from config.py
app.config.from_object('config')

# Init the mongo flask instance
mongo.init_app(app)

# you can also pass the key here if you prefer
GoogleMaps(app, key=secret.GOOGLEMAPS_KEY)

'''
Utilities
'''


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            session['username']
        except KeyError:
            return redirect(url_for('landing'))
        return f(*args, **kwargs)

    return decorated_function


'''
Web Page Routes
'''


@app.route("/", methods=['GET'])
def landing():
    return render_template("landing/index.html")


@app.route("/admin/login", methods=['POST'])
def login():
    if request.form['username'] and request.form['password']:
        form_username = request.form['username']
        form_password = request.form['password']
        form_hash = sha256(form_password).hexdigest()
        # check with db
        mcol = mongo.db['tribes-users']
        mdata = mcol.find_one({"username": form_username})
        if mdata:
            if form_hash == mdata['password']:
                session['username'] = request.form['username']
                return redirect(url_for('dashboard'))
    return redirect(url_for('landing'))


@app.route("/admin/logout", methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('landing'))


@app.route("/admin/dashboard", methods=['GET'])
@login_required
def dashboard():

    points = []

    r = requests.get(request.url_root + 'api/v1/data')
    time.sleep(1)

    for entry in r.json()['data']:
        item = {
            'icon': 'http://maps.google.com/mapfiles/ms/icons/green-dot.png',
            'lat': entry['location_lat'],
            'lng': entry['location_lon'],
            'infobox': "<b>" + entry['sensor_id'] + "</b>"
        }
        points.append(item)

    dashboard_map = Map(
        identifier="dashboard_map",
        style=(
            "height:100%;"
            "width:100%;"
            "top:0;"
            "left:0;"
            "min-height:500px;"
        ),
        lat=-31.9538,
        lng=115.8532,
        markers=points
    )
    return render_template("admin/dashboard.html", dashboard_map=dashboard_map)


@app.route("/ajax/data_insert", methods=['POST'])
def sensor_add():
    data = json.loads(request.data)

    sensor_id = data['sensor_id']
    sensor_mac = data['sensor_mac']
    location_lon = data['location_lon']
    location_lat = data['location_lat']
    timestamp = data['timestamp']

    entry = {
        'sensor_id': sensor_id,
        'sensor_mac': sensor_mac,
        'location_lon': location_lon,
        'location_lat': location_lat,
        'timestamp': timestamp
    }

    mongo.db['tribes-data'].insert_one(entry)


@app.route("/admin/databases", methods=['GET'])
@login_required
def databases():
    return render_template("admin/databases.html")


'''
API Definitions
'''
api = Api(app)

api.add_resource(Data, "/api/v1/data", "/api/v1/data/")

if __name__ == '__main__':
    app.run(host='0.0.0.0')
