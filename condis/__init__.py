from flask import Flask
import os


def create_app():
	""" Create the flask app instance"""
	
	app = Flask(__name__)
	# cel.conf.update(app.config)
	SECRET_KEY = os.urandom(32)
	app.config['SECRET_KEY'] = SECRET_KEY

	from condis.main.routes import main

	app.register_blueprint(main)

	return app