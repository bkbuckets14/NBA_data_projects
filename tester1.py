# from sqlalchemy import create_engine, Column, Integer, String
# from sqlalchemy.orm import declarative_base, sessionmaker

from nba_api.stats.endpoints import shotchartdetail
from nba_api.stats.static import players, teams
import pandas as pd

def JB_trial():
    player_id, team_id = get_player_and_team_ids("Jaylen Brown", "Boston Celtics")

    shotchart = shotchartdetail.ShotChartDetail(
        team_id=team_id,
        player_id=player_id,
        season_type_all_star='Regular Season',
        season_nullable='2024-25',
        context_measure_simple='FGA',  # Field Goal Attempts
        game_id_nullable=''            # leave empty for full season
    )

    jb_df = shotchart.get_data_frames()[0]
    jb_df.drop('GRID_TYPE', axis=1, inplace=True)

    return jb_df


def get_player_and_team_ids(player_name, team_name):
    player_id = players.find_players_by_full_name(player_name)[0]['id']
    team_id = teams.find_teams_by_full_name(team_name)[0]['id']
    return player_id, team_id

#JB_trial()


# DATABASE_URL = "mysql+mysqlconnector://root:admin@mysql_container:3306/basketball_db"

# engine = create_engine(DATABASE_URL, echo=True)  # echo=True logs SQL statements

# Base = declarative_base()

# class PlayByPlay(Base):
#     __tablename__ = 'playbyplay'

# class ShotChart(Base):
#     __tablename__ = 'shotchart'

#     game_id = Column(Integer)
#     game_event_id = Column(Integer)
#     player_id = Column(Integer)
#     player_name = Column(String(50))
#     team_id = Column(Integer)
#     team_name = Column(String(50))
#     period = Column(Integer)
#     minutes_remaining = Column(Integer)
#     seconds_remaining = Column(Integer)
#     event_type = Column(String(50))
#     action_type = Column(String(50))
#     shot_type = Column(String(50))
#     shot_zone_basic = Column(String(50))
#     shot_zone_area = Column(String(50))
#     shot_zone_range = Column(String(50))
#     shot_distance = Column(Integer)
#     loc_x = Column(Integer)
#     loc_y = Column(Integer)
#     shot_attempted_flag = Column(Integer)
#     shot_made_flag = Column(Integer)
#     game_date = Column(Integer)
#     htm = Column(String(5))
#     vtm = Column(String(5))



#     def __repr__(self):
#         return f"<User(name={self.name}, email={self.email})>"

# # Step 5: Create tables in the database
# Base.metadata.create_all(engine)

# # Step 6: Create a session
# Session = sessionmaker(bind=engine)
# session = Session()

# # Step 7: Insert data
# new_user = User(name="Alice", email="alice@example.com")
# session.add(new_user)
# session.commit()


# END OF DATABASE TESTING

# def JB_trial():
#     player_id, team_id = get_player_and_team_ids("Jaylen Brown", "Boston Celtics")

#     shotchart = shotchartdetail.ShotChartDetail(
#         team_id=team_id,
#         player_id=player_id,
#         season_type_all_star='Regular Season',
#         season_nullable='2024-25',
#         context_measure_simple='FGA',  # Field Goal Attempts
#         game_id_nullable=''            # leave empty for full season
#     )

#     jb_df = shotchart.get_data_frames()[0]
#     print(jb_df.loc[0])


# def get_player_and_team_ids(player_name, team_name):
#     player_id = players.find_players_by_full_name(player_name)[0]['id']
#     team_id = teams.find_teams_by_full_name(team_name)[0]['id']
#     return player_id, team_id

# JB_trial()

# # Example: filter by specific game
# # Replace with actual Game ID (e.g., "0022200001")
# game_id = "0022200001"
# shotchart_game = shotchartdetail.ShotChartDetail(
#     team_id=team_id,
#     player_id=player_id,
#     game_id_nullable=game_id,
#     context_measure_simple='FGA'
# )

# game_shot_df = shotchart_game.get_data_frames()[0]
# print(game_shot_df[['GAME_ID','PERIOD','MINUTES_REMAINING','LOC_X','LOC_Y','SHOT_MADE_FLAG']])

# BK Testing


