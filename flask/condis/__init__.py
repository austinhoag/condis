from flask import Flask
from celery import Celery
import redis
from datetime import timedelta
import datajoint as dj

def set_schema():
	dj.config['database.host'] = 'db'
	dj.config['database.user'] = 'root'
	dj.config['database.password'] = 'simple'
	dj.config['database.port'] = 3307
	# db_lightsheet = dj.create_virtual_module('lightsheet','u19lightserv_lightsheet',create_schema=True) # creates the schema if it does not already exist. Can't add tables from within the app because create_schema=False
	db = dj.create_virtual_module('test_db','test_db',create_schema=True) # creates the schema if it does not already exist. Can't add tables from within the app because create_schema=False
	
	return db

db = set_schema()

cel = Celery(__name__,broker='redis://redis:6379/0',
			backend='redis://redis:6379/0')

celery_beat_schedule = {
    'test_schedule': {
        'task': 'condis.main.tasks.send_daily_emails',
        'schedule': timedelta(seconds=3)
    },
}

def create_app():
	""" Create the flask app instance"""
	app = Flask(__name__)

	app.config['CELERYBEAT_SCHEDULE'] = celery_beat_schedule
	cel.conf.update(app.config)

	from condis.main.routes import main

	app.register_blueprint(main)

	return app

