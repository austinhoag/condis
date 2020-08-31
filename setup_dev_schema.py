import os
import datajoint as dj
dj.config['database.host'] = 'localhost'
dj.config['database.port'] = 3307
dj.config['database.user'] = 'user'
dj.config['database.password'] = 'pass'

os.environ['FLASK_MODE'] = 'DEV'

dev_schema = dj.schema('dev_db')

drop_schema = input("Drop dev schema? (yes or No): ")
if drop_schema == 'yes':
	# You have to drop the schemas that use the other schemas first
	# because if you try to drop a parent schema but a dependent schema
	# still exists then you will get a foreign key error
	dev_schema.drop(force=True)

from schemas import condis # this is enough to rebuild the schema