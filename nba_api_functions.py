from requests.exceptions import ReadTimeout

#nba_api packages
from nba_api.stats.endpoints import shotchartdetail, leaguegamelog
from nba_api.stats.static import players, teams

import pandas as pd

#function to load the shot records for all players in the 2024-25 season
def shotchart_2024_2025():
    #this gets all the players who played in the 2024-25 season and the teams they played for
    gamelog = leaguegamelog.LeagueGameLog(season='2024-25', player_or_team_abbreviation='P',season_type_all_star='Regular Season')
    gl_df = gamelog.get_data_frames()[0]
    player_df = gl_df[['PLAYER_ID', 'TEAM_ID']].drop_duplicates()
    #this gets the player_ids and team_ids and puts them into a list
    id_list = [{'player_id': player_id, 'team_id': team_id} for player_id, team_id in zip(player_df.PLAYER_ID, player_df.TEAM_ID)]
    print("Num Players:", len(id_list)) #to test out how many total players there will be

    #this is the list that will hold all the shot data
    shot_list = []

    #for each player_id, team_id pair
    for ind, id in enumerate(id_list):
        #tracker to check progress
        if ind%50 == 0:
            print('Data Received for', ind, 'players')

        try:
            #get the shot data for the player_id, team_id pair
            shotchart = shotchartdetail.ShotChartDetail(
                team_id=id['team_id'],
                player_id=id['player_id'],
                season_type_all_star='Regular Season',
                season_nullable='2024-25',
                context_measure_simple='FGA',  # Field Goal Attempts
                game_id_nullable=''            # leave empty for full season
            )

            #get the data as a dataframe
            results = shotchart.get_data_frames()[0]
            results.drop('GRID_TYPE', axis=1, inplace=True)
            results = results.astype(object)

            #append each shot to the shot_list
            for record in results.to_dict(orient='records'):
                shot_list.append(record)

        #if there is an error, print error, player_id, team_id
        except ReadTimeout as r:
            print(r)
            print("Player ID:", id['player_id'])
            print("Team ID:", id['team_id'])

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

#simple function to get a player_id and team_id
def get_player_and_team_ids(player_name, team_name):
    #get the player_id based on the player's name
    player_id = players.find_players_by_full_name(player_name)[0]['id']
    #get the team_id based on the team's name
    team_id = teams.find_teams_by_full_name(team_name)[0]['id']

    #return player_id and team_id as a tuple
    return player_id, team_id