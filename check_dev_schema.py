import os
import datajoint as dj
dj.config['database.host'] = 'localhost'
dj.config['database.port'] = 3307
dj.config['database.user'] = 'user'
dj.config['database.password'] = 'pass'

os.environ['FLASK_MODE'] = 'DEV'

dev_schema = dj.create_virtual_module('dev_db','dev_db')

print(dev_schema.schema)
print(dir(dev_schema))