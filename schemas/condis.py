import datajoint as dj

dj.config['database.host'] = 'localhost'
dj.config['database.port'] = 3307

dj.config['database.user'] = 'root'
dj.config['database.password'] = 'simple'

schema = dj.schema('test_db') 

@schema
class User(dj.Lookup):
    definition = """
    # Users
    email       : varchar(50)
    ---
    """

@schema
class GridSearchParams(dj.Lookup):
    definition = """
    # Keep track of each location that someone has entered. Users can have as many unique combinations as they want
    # so each column needs to be a primary key
    -> User
    latitude       : float
    longitude      : float
    min_time       : varchar(5)
    max_time       : varchar(5)
    grid_id        : varchar(3)
    grid_x         : smallint unsigned
    grid_y	       : smallint unsigned
    min_temp       : smallint unsigned
    max_temp       : smallint unsigned
    min_humidity   : smallint unsigned
    max_humidity   : smallint unsigned
	min_precip     : smallint unsigned
    max_precip     : smallint unsigned
    ---
    """