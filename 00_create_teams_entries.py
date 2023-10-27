from entry_comp import *
from formations import *
from teams import *
import pandas as pd
import os
from coach import *
from get_page import *
from check_acl_id import checkACLID

# Inputs Start

entry_df = pd.DataFrame(
    columns=["Id", "IdCompetition", "IdTeam", "Position", "Value1", "Value2"]
)

print("Loading Required Info...")

leagues_merge = pd.read_excel("Input/Leagues 22-to-21.xlsx")

id21 = leagues_merge["id21"].tolist()
id22 = leagues_merge["id22"].tolist()

entryids_counter = 1

game_page = get_page("https://www.pesmaster.com/efootball-2022/")

print("Loaded!")

leagues_urls = league_info_scrapper(game_page, "url")
# Inputs End
# Script start

# Irritate through leagues Ids with counter
for league_count, league_id22 in enumerate(league_info_scrapper(game_page, "id")):
    print()
    print(str(league_count + 1) + "/" + str(len(leagues_urls)))
    # Check wether Id of eFootball 22 in PES 21 in Leagues 22-to-21.xlsx
    try:
        league_id = id21[id22.index(int(league_id22))]
    except:
        # Set zero so it's skipped and added to other teams in-game
        # Should be changed manually in internal or external editor
        league_id = 0
    # Irritate through all teams in league entries
    for dict in league_scrapper(get_page(leagues_urls[league_count])):
        if league_id != 0:  # Real Entry
            # Appending in entires or revise according to later results
            dict["Id"] = str(entryids_counter)
            dict["IdCompetition"] = str(league_id)
            entry_df = pd.concat(
                [entry_df, pd.DataFrame(dict, index=[0])], ignore_index=True
            )
            # Get cup id to append teams of leagues to it, all teams participate
            cup_id = cup_id_scrapper(league_id)
            if cup_id != 0:
                # entry_df.loc[entry_df['IdCompetition']]
                entryids_counter += 1
                dict["Id"] = str(entryids_counter)
                dict["IdCompetition"] = str(cup_id)
                entry_df = pd.concat(
                    [entry_df, pd.DataFrame(dict, index=[0])], ignore_index=True
                )
            entryids_counter += 1
    # Get every team data in league and append to "LIST"
    for team_url in teams_urls_scrapper(get_page(leagues_urls[league_count])):
        print()
        team_page = get_page(team_url)
        team_id = checkACLID(str(team_url.split("/team/")[1].split("/")[0]))
        team_scrapper(team_page, team_id, leagues_merge)
        coach_id = str(coach_scrapper(team_page))
        formation_scrapper(team_page, team_id, coach_id)

if os.path.exists("Output") == False:
    os.mkdir("Output")

entry_df.to_csv("Output/Entry Competition - Bin.csv", index=False, sep=";")
createTeams()
createReviseTeams()
createTacticBins()
createCoaches()
