from rethinkdb import RethinkDB
from app.settings import Config

r = RethinkDB()

def connect_rethink():
    return r.connect(host=Config.RETHINK_HOST, port=Config.RETHINK_PORT, db=Config.RETHINK_DB)

