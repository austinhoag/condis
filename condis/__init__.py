from flask import (Flask,flash, render_template,
	request, redirect)
import redis
from datetime import timedelta
import os
from flask_wtf.csrf import CSRFProtect
from flask_wtf.csrf import CSRFError

import smtplib
import types

import datajoint as dj

def send_message_conditional(self,message): 
	"self is the smtp_server"
	if os.environ['FLASK_MODE'] == 'TEST': 
		print("not sending email because this is a test") 
	else: 
		print("sending email")
		smtplib.SMTP.send_message(self,message) 
		print("sent email")

funcType = types.MethodType
def smtp_connect():
	# Instantiate a connection object...
	print("Making SMTP connection")
	smtpObj = smtplib.SMTP('smtp.gmail.com',587)
	smtpObj.ehlo()
	smtpObj.starttls()
	smtpObj.login(os.environ.get('EMAIL_USER'),os.environ.get('EMAIL_PASS'))
	smtpObj.send_message = funcType(send_message_conditional,smtpObj)
	print("SMTP connection ready to send message")
	return smtpObj

def set_schema():
	if os.environ['FLASK_MODE'] == 'TEST':
		from schemas import condis
		dj.config['database.host'] = 'db'
		dj.config['database.user'] = 'root'
		dj.config['database.password'] = 'simple'
		dj.config['database.port'] = 3306 # inside the db container
		db = dj.create_virtual_module('test_db','test_db',create_schema=True) # creates the schema if it does not already exist. Can't add tables from within the app because create_schema=False
	if os.environ['FLASK_MODE'] == 'DEV':
		dj.config['database.host'] = 'db'
		dj.config['database.user'] = 'root'
		dj.config['database.password'] = 'simple'
		dj.config['database.port'] = 3306 # inside the db container
		db = dj.create_virtual_module('dev_db','dev_db') # creates the schema if it does not already exist. Can't add tables from within the app because create_schema=False
	elif os.environ['FLASK_MODE'] == 'PROD':
		dj.config['database.host'] = 'db'
		dj.config['database.user'] = 'root'
		dj.config['database.password'] = 'simple'
		dj.config['database.port'] = 3306 # inside the db container
		db = dj.create_virtual_module('condis_db','condis_db') 
	return db

db = set_schema()

def create_app():
	""" Create the flask app instance"""
	app = Flask(__name__)

	app.config['WTF_CSRF_TIME_LIMIT'] = 3600 # seconds
	SECRET_KEY = os.urandom(32)
	app.config['SECRET_KEY'] = SECRET_KEY

	csrf = CSRFProtect(app)

	from condis.main.routes import main

	app.register_blueprint(main)

	@app.errorhandler(CSRFError)
	def handle_csrf_error(e):
		""" If there is an CSRF Error anywhere in the application,
		this function will handle it - brings the user to a 500 error 
		page """
		print("There was a CSRF error")
		if e.description =='The CSRF token has expired.':
			csrf_time_limit_seconds = app.config['WTF_CSRF_TIME_LIMIT']
			csrf_time_limit_hours = csrf_time_limit_seconds/3600.
			flash(f"The form expired after {csrf_time_limit_hours} hours. "
			      f"Please continue completing the form within the next {csrf_time_limit_hours} hours.","warning")
		else:
			return render_template('errors/500.html')
		next_url = os.path.join('/',*request.url.split('?')[0].split('/')[3:])
		return redirect(next_url)
	return app

