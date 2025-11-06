import pickle

#nba_api packages
from nba_api.stats.endpoints import shotchartdetail, leaguegamelog, teamplayerdashboard
from nba_api.stats.static import players, teams

from datetime import datetime

import pandas as pd

def team_shotchart(team, season='2024-25'):

    #Load team_dict from pickle file
    with open("team_dict.pkl", "rb") as ff:
        team_dict = pickle.load(ff)
    
    #get the players from the team for a given season
    dashboard = teamplayerdashboard.TeamPlayerDashboard(
        team_id=team_dict[team],
        per_mode_detailed="Totals",
        season=season,
        season_type_all_star="Regular Season",
        date_from_nullable='10-21-2024'
    )
    
    #get the player_ids
    player_ids = dashboard.get_data_frames()[1].PLAYER_ID
    print("Number of Players on", team + ":", player_ids.size)

    #set up list to hold shots for a player and counter to count players
    shot_list = []
    counter = 0

    #for each player_id, team_id pair
    for player_id in player_ids:

        #get the players shots for the season
        shotchart = shotchartdetail.ShotChartDetail(
                team_id=team_dict[team],
                player_id=player_id,
                season_type_all_star='Regular Season',
                season_nullable='2024-25',
                context_measure_simple='FGA',  # Field Goal Attempts
                game_id_nullable=''            # leave empty for full season
        )
        
        #format the results from ShotChartDetail
        results = shotchart.get_data_frames()[0]
        results.drop('GRID_TYPE', axis=1, inplace=True)
        results = results.astype(object)

        #append each shot to the shot_list
        for record in results.to_dict(orient='records'):
            record['GAME_DATE'] = datetime.strptime(record["GAME_DATE"], "%Y%m%d").strftime("%Y-%m-%d") #reformat the date to work with SQL
            shot_list.append(record)

        #keep track of players added
        counter += 1
        print('Data Received for', counter, 'players')

    return shot_list

#trial function
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

#simple function to get a player_id and team_id
def get_player_and_team_ids(player_name, team_name):
    #get the player_id based on the player's name
    player_id = players.find_players_by_full_name(player_name)[0]['id']
    #get the team_id based on the team's name
    team_id = teams.find_teams_by_full_name(team_name)[0]['id']

    #return player_id and team_id as a tuple
    return player_id, team_id