import argparse
import password_parse as bk_pp #custom package/function to get DATABASE_URL from password file

#load in SQLAlchemy packages
from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.orm import declarative_base, sessionmaker

import nba_api_functions as bk_naf #custom package to interact with nba_api

#Parse argument for file name containing container name, database name, and root password.
parser = argparse.ArgumentParser(description="Read text file with database name and password.")
parser.add_argument("-p", "--pwd", type=argparse.FileType("r"), default=None, help="Path to file that contains container name, database name, and root password.")
args = parser.parse_args()

#Get DATABASE_URL using get_database_url function from password_parse
DATABASE_URL = bk_pp.get_database_url(args)

#create the engine to interact with Database
engine = create_engine(DATABASE_URL)  # echo=True logs SQL statements

#declaritive base to build tables from
Base = declarative_base()

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
    EVENT_TYPE = Column(String(25))
    ACTION_TYPE = Column(String(50))
    SHOT_TYPE = Column(String(25))
    SHOT_ZONE_BASIC = Column(String(30))
    SHOT_ZONE_AREA = Column(String(30))
    SHOT_ZONE_RANGE = Column(String(20))
    SHOT_DISTANCE = Column(Integer)
    LOC_X = Column(Integer)
    LOC_Y = Column(Integer)
    SHOT_ATTEMPTED_FLAG = Column(Integer)
    SHOT_MADE_FLAG = Column(Integer)
    GAME_DATE = Column(Date)
    HTM = Column(String(4))
    VTM = Column(String(4))


# create tables in the database
Base.metadata.create_all(engine)

# set up a session
Session = sessionmaker(bind=engine)
session = Session()

#list to handle multiple teams at a time
teams = ['Boston Celtics', 'Philadelphia 76ers', 'New York Knicks', 'Toronto Raptors', 'Brooklyn Nets']

for team in teams:
    # get shotchart data from nba_api_functions for a particular team
    data = bk_naf.team_shotchart(team=team)

    # insert data into the shotchart table
    for i, row in enumerate(data):
        new_shot_chart = ShotChart(**row)
        session.add(new_shot_chart)
        if i%1000==0:
            print(i, "rows added to database")

    # commit the data
    session.commit()

# test query for shot chart data
shots = session.query(ShotChart).all()
print("Total DB Size:", len(shots), "shots")

#close session (and dispose of old ones)
session.close()
engine.dispose()