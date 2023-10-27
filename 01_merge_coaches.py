import pandas as pd

fake_db = pd.read_csv("Input/Coaches - PES 2021 - Bin.csv", sep=";")
real_db = pd.read_excel(
    "Input/Every WE_PES Manager ID v08_07_2021, by NFS_FM.xlsx",
)

for counter in range(fake_db["Id"].count()):
    real_entry = real_db[
        real_db["Base ID"]
        == int(hex(fake_db.at[counter, "Id"]).replace("0x", "")[-5:], base=16)
    ]
    try:
        fake_db.at[counter, "Country"] = real_db.at[
            real_entry.index[0], "Nationality ID"
        ]
        fake_db.at[counter, "Name"] = real_db.at[real_entry.index[0], "Full real name"]
    except:
        pass

fake_db.to_csv("Input/Coaches - PES 2021 - Bin.csv", sep=";", index=False)
