import argparse
from password_parse import get_database_url

import sqlalchemy as db
import pandas as pd

parser = argparse.ArgumentParser(description="Read text file with database name and password.")
parser.add_argument("-p", "--pwd", type=argparse.FileType("r"), default=None, help="Path to file that contains container name, database name, and root password.")
args = parser.parse_args()
DATABASE_URL = get_database_url(args)

engine = db.create_engine(DATABASE_URL)

conn = engine.connect()

query = db.text('SELECT SHOT_ZONE_RANGE AS sb, COUNT(*) FROM shotchart GROUP BY SHOT_ZONE_RANGE')

exe = conn.execute(query)
result = exe.fetchall()
df = pd.DataFrame(data=result)
lens = [len(word) for word in df.sb]
print(df)
print(max(lens))

conn.close()