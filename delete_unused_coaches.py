import pandas as pd

coach = pd.read_csv("Input/Coaches - PES 2021 - Bin.csv", sep=";")
revise_team = pd.read_csv("Output/Revise Teams - Bin.csv", sep=";")
merged_team = pd.read_csv("Output/Teams - Bin.csv", sep=";")
full_team = pd.concat([revise_team, merged_team], ignore_index=True)
coachesUsed = full_team["Coach"].tolist()
final_coach = pd.DataFrame(columns=coach.columns)

for usedCoach in coachesUsed:
    final_coach.loc[len(final_coach.index)] = coach[coach["Id"] == usedCoach].iloc[0]
    # final_coach = pd.concat(
    #     [
    #         final_coach,
    #         pd.DataFrame(coach[coach["Id"] == usedCoach].iloc[0], index=[0]),
    #     ],
    #     ignore_index=True,
    # )
final_coach.to_csv("Output/Coaches - Bin.csv", index=False, sep=";")
