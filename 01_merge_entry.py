import pandas as pd

inferno = pd.read_csv("Input/Inferno - Entry.csv",
                      sep=";").sort_values(by=["Id"], ignore_index=True)
data = pd.read_csv("Input/Entry Competition - PES 2021 - Bin.csv",
                   sep=";").sort_values(by=["Id"], ignore_index=True)
competition = pd.read_csv(
    "Input/Competitions - PES 2021 - Bin.csv", sep=";").sort_values(by=["Id"], ignore_index=True)

for competitionId in range(0, competition['Id'].count()):
    infernoIndexes = []
    dataIndexes = []
    # print("Merging : " + competition.at[competitionId, "Name"])
    for entry in range(0, inferno["Id"].count()):
        if inferno.at[entry, "IdCompetition"] == competition.at[competitionId, "Id"]:
            infernoIndexes.append(entry)
    for entry in range(0, data["Id"].count()):
        if data.at[entry, "IdCompetition"] == competition.at[competitionId, "Id"]:
            dataIndexes.append(entry)
    if len(dataIndexes) < len(infernoIndexes):
        dataIndexes.append(data['Id'].count())
        data.at[data['Id'].count(), 'Id'] = data.at[data['Id'].count() - 1, 'Id'] + 1
    for counter, infernoIndex in enumerate(infernoIndexes):
        inferno.at[infernoIndex, "Id"] = data.at[dataIndexes[counter], "Id"]
        data.loc[dataIndexes[counter]] = inferno.loc[infernoIndex]

data.astype(int).to_csv('Input/Entry Competition - PES 2021 - Bin.csv',
                        sep=';', index=False)
