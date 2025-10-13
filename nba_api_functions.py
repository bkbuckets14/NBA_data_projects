from nba_api.stats.endpoints import shotchartdetail, playerindex
from nba_api.stats.static import players, teams
import pandas as pd

def shotchart_2024_2025():
    player_df = playerindex.PlayerIndex(season='2024-25').get_data_frames()[0]
    id_list = [{'player_id': player_id, 'team_id': team_id} for player_id, team_id in zip(player_df.PERSON_ID, player_df.TEAM_ID)]

    shot_list = []

    for id in id_list:
        shotchart = shotchartdetail.ShotChartDetail(
            team_id=id['team_id'],
            player_id=id['player_id'],
            season_type_all_star='Regular Season',
            season_nullable='2024-25',
            context_measure_simple='FGA',  # Field Goal Attempts
            game_id_nullable=''            # leave empty for full season
        )

        results = shotchart.get_data_frames()[0]
        results.drop('GRID_TYPE', axis=1, inplace=True)
        results = results.astype(object)

        for record in results.to_dict(orient='records'):
            shot_list.append(record)

    return shot_list


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

    results = shotchart.get_data_frames()[0]
    results.drop('GRID_TYPE', axis=1, inplace=True)
    results = results.astype(object)

    return results.to_dict(orient='records')


def get_player_and_team_ids(player_name, team_name):
    player_id = players.find_players_by_full_name(player_name)[0]['id']
    team_id = teams.find_teams_by_full_name(team_name)[0]['id']
    return player_id, team_id