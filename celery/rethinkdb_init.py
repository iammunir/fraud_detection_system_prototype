import os
from rethinkdb import RethinkDB

r = RethinkDB()

# Get environment variables
rethink_host = os.getenv("RETHINK_HOST", "localhost")
rethink_port = int(os.getenv("RETHINK_PORT", 28015))
rethink_db = os.getenv("RETHINK_DB", "fraud_detection")
required_tables = ["transactions"]

try:
    # Connect to RethinkDB
    conn = r.connect(host=rethink_host, port=rethink_port)

    # Check if the database exists
    if rethink_db not in r.db_list().run(conn):
        # Create the database
        r.db_create(rethink_db).run(conn)
        print(f"Database '{rethink_db}' created successfully.")
    else:
        print(f"Database '{rethink_db}' already exists.")

    # Switch to the database
    db = r.db(rethink_db)

    # Check and create the required tables
    existing_tables = db.table_list().run(conn)
    for table in required_tables:
        if table not in existing_tables:
            db.table_create(table).run(conn)
            print(f"Table '{table}' created successfully.")
        else:
            print(f"Table '{table}' already exists.")

    conn.close()
    
except Exception as e:
    print(f"Error connecting to RethinkDB or creating tables: {e}")