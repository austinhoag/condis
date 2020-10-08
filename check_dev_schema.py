import os
import datajoint as dj
dj.config['database.host'] = 'localhost'
dj.config['database.port'] = 3307
dj.config['database.user'] = os.environ['DB_USER']
dj.config['database.password'] = os.environ['DB_PASS']

os.environ['FLASK_MODE'] = 'DEV'

dev_schema = dj.create_virtual_module('dev_db','dev_db')

print(dev_schema.schema)
print(dir(dev_schema))