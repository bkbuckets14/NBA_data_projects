from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

import nba_api_functions as naf

#database URL for connection
DATABASE_URL = "mysql+mysqlconnector://root:admin@mysql_container:3306/basketball_db"

#create the engine to interact with Database
engine = create_engine(DATABASE_URL)  # echo=True logs SQL statements

#declaritive base to build tables from
Base = declarative_base()

# class PlayByPlay(Base):
#     __tablename__ = 'playbyplay'

#ShotChart class/table
class ShotChart(Base):
    __tablename__ = 'shotchart'

    ID = Column(Integer, primary_key=True, autoincrement=True)
    GAME_ID = Column(Integer)
    GAME_EVENT_ID = Column(Integer)
    PLAYER_ID = Column(Integer)
    PLAYER_NAME = Column(String(40))
    TEAM_ID = Column(Integer)
    TEAM_NAME = Column(String(25))
    PERIOD = Column(Integer)
    MINUTES_REMAINING = Column(Integer)
    SECONDS_REMAINING = Column(Integer)
    EVENT_TYPE = Column(String(50)) #What is the longest?
    ACTION_TYPE = Column(String(50)) #What is the longest?
    SHOT_TYPE = Column(String(50)) #What is the longest?
    SHOT_ZONE_BASIC = Column(String(50)) #What is the longest?
    SHOT_ZONE_AREA = Column(String(50)) #What is the longest?
    SHOT_ZONE_RANGE = Column(String(50)) #What is the longest?
    SHOT_DISTANCE = Column(Integer)
    LOC_X = Column(Integer)
    LOC_Y = Column(Integer)
    SHOT_ATTEMPTED_FLAG = Column(Integer)
    SHOT_MADE_FLAG = Column(Integer)
    GAME_DATE = Column(Integer)
    HTM = Column(String(4))
    VTM = Column(String(4))


# create tables in the database
Base.metadata.create_all(engine)

# set up a session
Session = sessionmaker(bind=engine)
session = Session()

# get shotchart data from nba_api_functions
data = naf.shotchart_2024_2025()

# insert data into the shotchart table
for i, row in enumerate(data):
    new_shot_chart = ShotChart(**row)
    session.add(new_shot_chart)
    if i%10000==0:
        print(i, "rows added to database")

# commit the data
session.commit()

# test query for shot chart data
shots = session.query(ShotChart).limit(15).all()
for shot in shots:
    print(shot.ID, shot.GAME_EVENT_ID, shot.SHOT_ZONE_BASIC)

#close session (and dispose of old ones)
session.close()
engine.dispose()