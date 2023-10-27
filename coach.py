from urllib import response
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
import os

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}

fake_db = pd.read_csv("Input/Coaches - PES 2021 - Bin.csv", sep=";")
real_db = pd.read_excel(
    "Input/Every WE_PES Manager ID v08_07_2021, by NFS_FM.xlsx",
)


def coach_url_scrapper(r: response):
    soup = bs(r.content, "html.parser")

    coach_url = (
        "https://www.pesmaster.com"
        + soup.find("div", attrs={"class": "coach-container"}).find("a")["href"]
    )
    return coach_url


def coach_scrapper(team_r):
    coach_info = []
    coach_url = coach_url_scrapper(team_r)
    coach_id = int(coach_url.split("/coach/")[1].split("/")[0])
    real_coach_id = int(hex(coach_id).replace("0x", "")[-5:], base=16)
    real_entry = real_db[real_db["Base ID"] == real_coach_id]
    fake_entry = fake_db[fake_db["Id"] == coach_id]
    if real_entry.empty:
        r = requests.get(coach_url, headers=headers)
        soup = bs(r.content, "html.parser")
        for info in soup.find("table", attrs={"class": "player-info"}).find_all("td"):
            info = info.text.strip()
            coach_info.append(info)
        fake_bool = coach_info[coach_info.index("Type") + 1] == "Fake"
        try:
            coach_name = coach_info[coach_info.index("Full Name") + 1]
        except:
            if fake_bool:
                coach_name = coach_info[coach_info.index("Real Name") + 1]
        if not fake_bool or coach_name == "-":
            coach_name = coach_info[coach_info.index("Name") + 1]
        if fake_entry.empty:
            fake_db.loc[len(fake_db.index)] = [
                coach_id,
                coach_name,
                228,
                "",
                100,
                0,
                "",
                False,
                False,
                False,
                False,
                0,
                0,
                0,
                -1,
                -1,
                -1,
            ]
            print("Created Coach")
        else:
            fake_db.at[fake_entry.index[0], "Name"] = coach_name
    else:
        coach_name = real_db.at[real_entry.index[0], "Full real name"]
        if fake_entry.empty:
            fake_db.loc[len(fake_db.index)] = [
                coach_id,
                coach_name,
                real_db.at[real_entry.index[0], "Nationality ID"],
                "",
                100,
                0,
                "",
                False,
                False,
                False,
                False,
                0,
                0,
                0,
                -1,
                -1,
                -1,
            ]
            print("Created Coach")
        # This step was already done in 01_merge_coaches

        # else:
        #     try:
        #         fake_db.at[counter, "Country"] = real_db.at[
        #             real_entry.index[0], "Nationality ID"
        #         ]
        #         fake_db.at[counter, "Name"] = real_db.at[real_entry.index[0], "Full real name"]
        #     except:
        #         pass

    print("Coach : " + coach_name)
    return coach_id


def createCoaches():
    fake_db.to_csv("Input/Coaches - PES 2021 - Bin.csv", sep=";", index=False)
