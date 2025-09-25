# pip install nba_api

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
    print(jb_df.columns)


def get_player_and_team_ids(player_name, team_name):
    player_id = players.find_players_by_full_name(player_name)[0]['id']
    team_id = teams.find_teams_by_full_name(team_name)[0]['id']
    return player_id, team_id

JB_trial()

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
