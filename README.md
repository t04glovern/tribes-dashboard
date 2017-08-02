# Installation
Add a `secret.py` file with the password hash (get it from Nathan) if you want to run it locally.

The `tribes.sh` script is setup for the an nginx hosting with the site added as a service to systemd. I'm also using a virtualenv in my home directory. None of these are really required for running it locally.

Use python 2.7

### Setting up service

Add something similar to the following to your **/etc/systemd/system/tribes.service** file

```bash
[Unit]
Description=Gunicorn instance to serve Tribes Dashboard
After=network.target

[Service]
User=nathan
Group=www-data
WorkingDirectory=/home/nathan/Production/tribes-dashboard
Environment="PATH=/home/nathan/.virtualenvs/flask-python2.7-dev/bin"
ExecStart=/home/nathan/.virtualenvs/flask-python2.7-dev/bin/gunicorn --workers 3 --bind unix:tribes.sock -m 007 wsgi:app

[Install]
WantedBy=multi-user.target
```
