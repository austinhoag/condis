import os
import datajoint as dj
dj.config['database.host'] = 'localhost'
dj.config['database.port'] = 3307
dj.config['database.user'] = 'user'
dj.config['database.password'] = 'pass'

os.environ['FLASK_MODE'] = 'PROD'

from schemas import condis # this is enough to rebuild the schema