import pandas as pd

revise_data = pd.read_csv("Output/Revise Teams - Bin.csv", sep=";")
merged_data = pd.read_csv("Output/Teams - Bin.csv", sep=";")
full_data = pd.concat([revise_data, merged_data], ignore_index=True)
entry_data = pd.read_csv("Output/Entry Competition - Bin.csv", sep=";")
print("Reminder : Please Revise files that require revision before running that script")
for counter in range(full_data["Id"].count()):
    if (
        hex(full_data.at[counter, "Id"])[2:].startswith("40")
        and full_data.at[counter, "National"] == False
    ):
        entry_data.at[
            entry_data[entry_data["IdTeam"] == full_data.at[counter, "Id"]].index[0],
            "IdTeam",
        ] = int("0x" + hex(full_data.at[counter, "Id"])[4:], base=16)
        full_data.drop(
            full_data[full_data["Id"] == full_data.at[counter, "Id"]].index,
            inplace=True,
        )

full_data.sort_values(by="Id").to_csv(
    "Output/NoACL - Teams - Bin.csv", index=False, sep=";"
)
entry_data.to_csv("Output/NoACL - Entry Competition - Bin.csv", index=False, sep=";")
