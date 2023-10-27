import pandas as pd
from get_page import *
from bs4 import BeautifulSoup as bs

# MAX X = 43    (at Top)
# MIN X = 3     (at Bottom (GK))
# MAX Y = 94    (at Right)
# MIN Y = 10    (at Left)
# CENTER Y = 52

position_dict = {
    "CB": "1",
    "LB": "2",
    "RB": "3",
    "DMF": "4",
    "CMF": "5",
    "LMF": "6",
    "RMF": "7",
    "AMF": "8",
    "LWF": "9",
    "RWF": "10",
    "SS": "11",
    "CF": "12",
}

formations_df = pd.DataFrame(
    columns=[
        "Id",  # Counter
        "IdTactic",  # Coach Id
        "NumFormation",  # Game has 3 identical lineups (0, 1, 2)
        "NumPlayer",  # (0-10)
        "Position",  # Game Plan Position
        "LocationX",  # Top
        "LocationY",  # Left
        "A",  # 0
        "B",  # 0
    ]
)

old_tactics_df = pd.read_csv("Input/Tactics - PES 2021 - Bin.csv", sep=";")
new_tactics_df = pd.DataFrame(columns=old_tactics_df.columns)

counter = 1


def formation_scrapper(r, team_id, coach_id):
    global counter
    global formations_df
    global new_tactics_df
    # Tactic
    try:
        target_tactic = old_tactics_df[old_tactics_df["IdTeam"] == int(team_id)].iloc[
            [0]
        ]
        target_tactic["Id"] = coach_id
        target_tactic["NumStrategy"] = 0
        new_tactics_df = pd.concat(
            [
                new_tactics_df,
                target_tactic,
            ],
            ignore_index=True,
            axis=0,
        )
    except:  # No Tactic Found
        target_tactic = {
            "Id": coach_id,
            "IdTeam": team_id,
            # No idea what those values stand for.
            # Based on Man City values
            "AttackingStyles": "1",
            "BuildUp": "1",
            "AttackingArea": "1",
            "Positioning": "1",
            "SupportRange": "2",
            "NumbersInAttack": "2",
            "DefensiveStyles": "0",
            "ContainmentArea": "0",
            "Pressuring": "0",
            "DefensiveLine": "10",
            "Compactness": "1",
            "NumbersInDefense": "0",
            "NumStrategy": "0",
            "Value1": "0",  # Varies, 0 is safest
            "A": "0",  # 0
        }
        new_tactics_df = pd.concat(
            [new_tactics_df, pd.DataFrame(target_tactic, index=[0])], ignore_index=True
        )
        print("Created Tactic")
    # Formation
    soup = bs(r.content, "html.parser")
    lineup = []
    for NumPlayerCounter, playerDiv in enumerate(
        soup.find(
            "div", attrs={"class": "game-plan-container gp-container-new"}
        ).find_all("div", attrs={"class": "gp-player"})
    ):
        try:
            coordinates = playerDiv.attrs["style"].split(";")
            for NumFormation in range(3):
                lineup.append(
                    {
                        "Id": counter,
                        "IdTactic": coach_id,
                        "NumFormation": str(NumFormation),
                        "NumPlayer": NumPlayerCounter,
                        "Position": position_dict[
                            playerDiv.find(
                                "div", attrs={"class": "gp-player-pos"}
                            ).text.strip()
                        ],
                        "LocationX": str(
                            (
                                float(coordinates[0].split("top: ")[1][:-1]) * -1 / 2
                            ).__round__()
                            + 43
                        ),
                        "LocationY": str(
                            float(coordinates[1].split("left: ")[1][:-1]).__round__()
                            + 12
                        ),
                        "A": "0",
                        "B": "0",
                    }
                )
                counter += 1
        except:  # GK doesn't have style attribute
            for NumFormation in range(3):
                lineup.append(
                    {
                        "Id": counter,
                        "IdTactic": coach_id,
                        "NumFormation": str(NumFormation),
                        "NumPlayer": NumPlayerCounter,
                        "Position": "0",
                        "LocationX": "3",
                        "LocationY": "52",
                        "A": "0",
                        "B": "0",
                    }
                )
                counter += 1
    formations_df = pd.concat(
        [formations_df, pd.DataFrame(data=lineup)], ignore_index=True
    )


def createTacticBins():
    formations_df.to_csv("Output/Formations - Bin.csv", index=False, sep=";")
    new_tactics_df.to_csv("Output/Tactics - Bin.csv", index=False, sep=";")
