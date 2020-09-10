import os, sys
if os.environ.get('FLASK_MODE') != 'TEST':
	raise KeyError("Must set environmental variable FLASK_MODE=TEST")
from flask import url_for,request
import pytest
import datajoint as dj
from condis import create_app,db

user_agent_str = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36'
user_agent_str_firefox = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.14; rv:72.0) Gecko/20100101 Firefox/72.0'

""" Fixtures for different test clients (different browsers) """

@pytest.fixture(scope='session') 
def test_client():
	""" Create the application and the test client.
	The way a fixture works is whaterver is yielded
	by this function will be passed to the tests that 
	take the name of the fixture function as an argument.
	We use scope='module' because we only want the test_client
	to last for tests in a single module. If we use scope='session',
	then the state of the test client will be altered by one test module,
	and then that is the state of the client when the next test module
	is executed. This will mean the test order will matter which is a 
	bad way to do things. It does mean we will have to reload the
	test client in each module in which we use it, so it is slightly slower this way."" 
	"""
	print('----------Setup test client----------')

	app = create_app()
	app.config['WTF_CSRF_ENABLED'] = False
	testing_client = app.test_client()

	""" Simulate a chrome user """
	testing_client.environ_base["HTTP_USER_AGENT"] = user_agent_str

	ctx = app.test_request_context() # makes it so I can use the url_for() function in the tests
	ctx.push()
	yield testing_client # this is where the testing happens
	print('-------Teardown test client--------')
	""" Drop all schemas """
	db.schema.drop(force=True)

	ctx.pop()