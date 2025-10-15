import sqlalchemy as db
import pandas as pd

DATABASE_URL = "mysql+mysqlconnector://root:admin@mysql_container:3306/basketball_db"

engine = db.create_engine(DATABASE_URL)

conn = engine.connect()

query = db.text('SELECT SHOT_TYPE, COUNT(*) FROM shotchart WHERE PLAYER_ID=1628369 GROUP BY SHOT_TYPE')

exe = conn.execute(query)
result = exe.fetchall()
df = pd.DataFrame(data=result)
print(df)

conn.close()