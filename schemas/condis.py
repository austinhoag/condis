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
    """