import os
import datajoint as dj
dj.config['database.host'] = 'localhost'
dj.config['database.port'] = 3307
dj.config['database.user'] = os.environ['DB_USER']
dj.config['database.password'] = os.environ['DB_PASS']

os.environ['FLASK_MODE'] = 'PROD'

from schemas import condis # this is enough to rebuild the schema