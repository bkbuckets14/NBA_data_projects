import argparse
from password_parse import get_database_url #custom package/function to get DATABASE_URL from password file

import sqlalchemy as db
import pandas as pd

#Parse argument for file name containing container name, database name, and root password.
parser = argparse.ArgumentParser(description="Read text file with database name and password.")
parser.add_argument("-p", "--pwd", type=argparse.FileType("r"), default=None, help="Path to file that contains container name, database name, and root password.")
args = parser.parse_args()

#Get DATABASE_URL using get_database_url function from password_parse
DATABASE_URL = get_database_url(args)

#create the engine to interact with Database
engine = db.create_engine(DATABASE_URL)

df = pd.read_sql("SELECT * FROM basketball_db", engine)

#connect to engine
#conn = engine.connect()

#query to run
#query = db.text('SELECT SHOT_ZONE_RANGE AS sb, COUNT(*) FROM shotchart GROUP BY SHOT_ZONE_RANGE')

#execute query
#exe = conn.execute(query)
#result = exe.fetchall()
#df = pd.read_sql("SELECT * FROM basketball_db WHERE PLAYER_NAME = 'Jaylen Brown'", engine)
print(df)

#close connection (and dispose of old ones)
conn.close()
engine.dispose()