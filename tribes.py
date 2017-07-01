from flask import Flask, render_template, request, redirect, session, url_for
from functools import wraps
from hashlib import sha256

import secret

## Flask_MongoDB imports
from mongo import mongo

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
    return render_template("admin/dashboard.html")


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
