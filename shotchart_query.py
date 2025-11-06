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

#simple query to get all columns from the shotchart database
df = pd.read_sql("SELECT * FROM shotchart", engine)
print(df)

#query to get the number of shot attempts per player on the Boston Celtics from most to least shots
df2 = pd.read_sql("SELECT PLAYER_NAME, Count(*) as FGAs FROM shotchart WHERE TEAM_NAME='Boston Celtics' GROUP BY PLAYER_NAME ORDER BY FGAs DESC ", engine)
print(df2)

#fully dispose of engine
engine.dispose()