from urllib import response
import pandas as pd
from bs4 import BeautifulSoup as bs
from get_page import get_page
from unidecode import unidecode


datalist = pd.read_csv("Input/Teams - PES 2021 - Bin.csv", sep=";")

impid = datalist["Id"].tolist()
leagues_names = []
countries = []

teams_df = pd.DataFrame(columns=datalist.columns)
revise_teams_df = pd.DataFrame(columns=datalist.columns)

teamAbbrev = [
    "AC ",
    " CF",
    " FC",
    # ' de ',
    "SSC ",
    "SS ",
    " BC",
    "AS ",
    "US ",
    " GR",
    "LOSC ",
    "AJ ",
    # ' SCO',
    "ESTAC ",
    "OGC ",
    "RC ",
    "RCD ",
    "CA ",
    "UD ",
    " UD",
    "CD ",
    "SD ",
    " SK",
    " AC",
    " NB",
    " AB",
    " VB",
    " JK",
    " FK",
    " EC",
    " PB",
    " PW",
    " RW",
    " BZ",
    " GZ",
    " ZW",
    " BW",
    " WZRG",
    " GR",
    " RWZ",
    " BG",
    " GB",
    " A",
    " RB",
    " G",
    " NN",
]


def removeAbbrev(teamName: str):
    teamName = teamName.replace("-", " ")
    if len(teamName.split(" ")) > 1:
        for abbrev in teamAbbrev:
            if teamName.startswith(abbrev) or teamName.endswith(abbrev):
                teamName = teamName.replace(abbrev, "")
    return teamName


def return_null(s):
    i = str(s)
    if i == "nan":
        i = ""
    return i


def teams_urls_scrapper(r: response):
    urls = []
    soup = bs(r.content, "html.parser")
    for team_url_div in soup.find(
        "div", attrs={"class": "team-block-container"}
    ).find_all("div", attrs={"class": "team-block"}):
        urls.append(
            "https://www.pesmaster.com/"
            + team_url_div.find("a").get_attribute_list("href")[0]
        )
    return urls


def team_scrapper(
    r: response,
    team_id: str,
    leagues_merge: pd.DataFrame,
    team_url: str,
    league_id: int,
    national_bool: str,
    asian_national: bool,
):
    global teams_df
    global revise_teams_df
    country_index = ""
    soup = bs(r.content, "html.parser")
    team_name = removeAbbrev(soup.find("h1").text.strip())
    if team_name.endswith(")") == True:
        team_name = team_name.split("(")[1].replace(")", "")

    try:
        index = impid.index(int(team_id))
        impbool = True
    except:
        print("Created Team")
        impbool = False
    league_name = soup.find("a", attrs={"class": "namelink"}).text.strip()
    # league_id = int(
    #     soup.find("a", attrs={"class": "namelink"})
    #     .attrs["href"]
    #     .split("/league/")[1]
    #     .replace("/", "")
    # )

    try:
        country_index = leagues_names.index(league_id)
    except:
        country_index = ""
        if impbool == True:
            leagues_names.append(league_id)
            countries.append(return_null(datalist.at[index, "Country"]))
    # Already Found
    coach_id = (
        soup.find("div", attrs={"class": "coach-container"})
        .find("div", attrs={"class": "coach-container-name"})
        .find("a")
        .get_attribute_list("href")[0]
        .split("/coach/")[1]
        .split("/")[0]
    )
    if "National" in league_name:
        national_bool = "True"
        if asian_national:  # Grab AFC Asian Cup Team if found
            new_team_id = int(team_id) + 65536
            new_team_url = team_url.replace(team_id, str(new_team_id))
            new_r = get_page(new_team_url)
            if new_r.status_code == 200:
                print("ACL FOUND")
                return team_scrapper(
                    new_r,
                    team_id,
                    leagues_merge,
                    team_url,
                    league_id,
                    "True",
                    False,
                )
    NameEnglish = team_name
    NameUSEnglish = team_name
    NonPlayableLeague = "0"
    if league_name.find("Other") != -1:
        if league_name.find("Euro") != -1:
            NonPlayableLeague = "1"
        if league_name.find("Latin") != -1:
            NonPlayableLeague = "2"
        if league_name.find("Africa") != -1:
            NonPlayableLeague = "3"
        if league_name.find("Classic") != -1:
            NonPlayableLeague = "4"
        if team_name.find("Default") != -1:
            NonPlayableLeague = "5"
        if team_name.find("Asia") != -1:
            NonPlayableLeague = "6"
    try:
        if not leagues_merge[leagues_merge["other_europe_id"] == league_id].empty:
            NonPlayableLeague = "1"
    except:
        pass
    try:
        if not leagues_merge[leagues_merge["other_latin_id"] == league_id].empty:
            NonPlayableLeague = "2"
    except:
        pass
    try:
        if not leagues_merge[leagues_merge["other_asia_id"] == league_id].empty:
            NonPlayableLeague = "6"
    except:
        pass

    # Import
    if impbool == False:
        # Needed
        if country_index == "":
            country = "STILL MISSING"
        else:
            country = str(countries[country_index])
        if league_id == 266 or league_id == 101:  # J1 & AFC
            country = "13"
        elif league_id == 603 or league_id == 635:  # MLS & USL
            country = "135"
        elif league_id == 128:  # LIGA NOS
            country = "228"
        elif league_id == 476:  # SUPER TOTO
            country = "190"
        elif league_id == 346:  # SERIE BKT
            country = "215"
        elif league_id == 465:  # MEXICO
            country = "124"
        elif league_id == 152:  # ARGENTINA
            country = "144"

        if int(team_id) == 5749:  # INDIA
            country = "9"
        elif int(team_id) == 5750:  # INDONESIA
            country = "10"
        elif int(team_id) == 5752:  # MALAYSIA
            country = "21"
        elif int(team_id) == 1099:  # CANADA
            country = "110"
        elif int(team_id) == 232:  # WOLFSBURG
            country = "210"
        stadium_id = "29"  # KONAMI Stadium
        NameJapanese = ""
        NameSpanish = ""
        NameLatamSpanish = ""
        NameItalian = ""
        NamePortuguese = ""
        NameBrazilian = ""
        NameFrench = ""
        NameGerman = ""
        NameDutch = ""
        NameSwedish = ""
        NameRussian = ""
        NameGreek = ""
        NameTurkish = ""
        NameSimplifiedChinese = ""
        ShortNameLicensed = unidecode(
            team_name.replace(" ", "").replace(".", "").upper()[:3]
        )
        ShortNameFake = ShortNameLicensed
        LicencedCoach = "True"
        LicencedCoach2 = "True"
        HasAnthem = "False"  # Available only for SOME national teams
        AnthemStandingStyle = "0"
        AnthemPlayersSinging = "0"
        AnthemStandingAngle = "0"
        Team2020_2 = "0"
        Team2020_3 = "0"
        Team2020_4 = "0"
        Team2020_6 = "0"
        Team2020_9 = "0"
        Team2020_10 = "0"
        Team2020_11 = "0"
        Country2020_1 = "0"
        Country2020_2 = "0"
        Country2020_3 = "0"
        Country2020_4 = "0"
        Country2020_5 = "0"
        Value2020_1 = "0"
        Value2020_2 = "0"
        Value2020_3 = "-1"
        Value2020_4 = "0"
        Value2020_5 = "0"
        Value2020_6 = "0"
        Value2020_7 = "0"
        Value2020_8 = "0"
        Value2020_9 = "0"
        Value2020_10 = "0"
    if impbool == True:
        country = return_null(datalist.at[index, "Country"])
        stadium_id = return_null(datalist.at[index, "Stadium"])
        NameJapanese = return_null(datalist.at[index, "NameJapanese"])
        NameSpanish = return_null(datalist.at[index, "NameSpanish"])
        NameLatamSpanish = return_null(datalist.at[index, "NameLatamSpanish"])
        NameItalian = return_null(datalist.at[index, "NameItalian"])
        NamePortuguese = return_null(datalist.at[index, "NamePortuguese"])
        NameBrazilian = return_null(datalist.at[index, "NameBrazilian"])
        NameFrench = return_null(datalist.at[index, "NameFrench"])
        NameGerman = return_null(datalist.at[index, "NameGerman"])
        NameDutch = return_null(datalist.at[index, "NameDutch"])
        NameSwedish = return_null(datalist.at[index, "NameSwedish"])
        NameRussian = return_null(datalist.at[index, "NameRussian"])
        NameGreek = return_null(datalist.at[index, "NameGreek"])
        NameTurkish = return_null(datalist.at[index, "NameTurkish"])
        NameSimplifiedChinese = return_null(datalist.at[index, "NameSimplifiedChinese"])
        ShortNameLicensed = return_null(datalist.at[index, "ShortNameLicensed"])
        ShortNameFake = ShortNameLicensed
        LicencedCoach = return_null(datalist.at[index, "LicencedCoach"])
        LicencedCoach2 = return_null(datalist.at[index, "LicencedCoach2"])
        HasAnthem = return_null(datalist.at[index, "HasAnthem"])
        AnthemStandingStyle = return_null(datalist.at[index, "AnthemStandingStyle"])
        AnthemPlayersSinging = return_null(datalist.at[index, "AnthemPlayersSinging"])
        AnthemStandingAngle = return_null(datalist.at[index, "AnthemStandingAngle"])
        Team2020_2 = return_null(datalist.at[index, "Team2020_2"])
        Team2020_3 = return_null(datalist.at[index, "Team2020_3"])
        Team2020_4 = return_null(datalist.at[index, "Team2020_4"])
        Team2020_6 = return_null(datalist.at[index, "Team2020_6"])
        Team2020_9 = return_null(datalist.at[index, "Team2020_9"])
        Team2020_10 = return_null(datalist.at[index, "Team2020_10"])
        Team2020_11 = return_null(datalist.at[index, "Team2020_11"])
        Country2020_1 = return_null(datalist.at[index, "Country2020_1"])
        Country2020_2 = return_null(datalist.at[index, "Country2020_2"])
        Country2020_3 = return_null(datalist.at[index, "Country2020_3"])
        Country2020_4 = return_null(datalist.at[index, "Country2020_4"])
        Country2020_5 = return_null(datalist.at[index, "Country2020_5"])
        Value2020_1 = return_null(datalist.at[index, "Value2020_1"])
        Value2020_2 = return_null(datalist.at[index, "Value2020_2"])
        Value2020_3 = return_null(datalist.at[index, "Value2020_3"])
        Value2020_4 = return_null(datalist.at[index, "Value2020_4"])
        Value2020_5 = return_null(datalist.at[index, "Value2020_5"])
        Value2020_6 = return_null(datalist.at[index, "Value2020_6"])
        Value2020_7 = return_null(datalist.at[index, "Value2020_7"])
        Value2020_8 = return_null(datalist.at[index, "Value2020_8"])
        Value2020_9 = return_null(datalist.at[index, "Value2020_9"])
        Value2020_10 = return_null(datalist.at[index, "Value2020_10"])
    dict = {
        "Id": team_id,
        "Name": team_name,
        "Country": country,
        "Stadium": stadium_id,
        "Coach": coach_id,
        "National": national_bool,
        "NameJapanese": NameJapanese,
        "NameSpanish": NameSpanish,
        "NameLatamSpanish": NameLatamSpanish,
        "NameEnglish": NameEnglish,
        "NameUSEnglish": NameUSEnglish,
        "NameItalian": NameItalian,
        "NamePortuguese": NamePortuguese,
        "NameBrazilian": NameBrazilian,
        "NameFrench": NameFrench,
        "NameGerman": NameGerman,
        "NameDutch": NameDutch,
        "NameSwedish": NameSwedish,
        "NameRussian": NameRussian,
        "NameGreek": NameGreek,
        "NameTurkish": NameTurkish,
        "NameSimplifiedChinese": NameSimplifiedChinese,
        "NameDatabase": team_name,
        "NameEmpty1": "",
        "NameEmpty2": "",
        "NameEmpty3": "",
        "NameEmpty4": "",
        "ShortNameLicensed": ShortNameLicensed,
        "ShortNameFake": ShortNameFake,
        "Abbreviation": "",
        "Commentary": "-1",
        "StadiumFile": "-1",
        "StadiumName": "",
        "StadiumFileName": "",
        "EmblemFile": "-1",
        "EmblemFileName": "",
        "Rival1": "0",
        "Rival2": "0",
        "Rival3": "0",
        "Banner1": "",
        "Banner2": "",
        "Banner3": "",
        "Banner4": "",
        "Kit1": "0",
        "Kit2": "0",
        "Kit3": "0",
        "Kit4": "0",
        "Kit5": "0",
        "Kit6": "0",
        "Kit7": "0",
        "Kit8": "0",
        "Kit9": "0",
        "Kit10": "0",
        "TeamColor1R": "0",
        "TeamColor1G": "0",
        "TeamColor1B": "0",
        "TeamColor2R": "0",
        "TeamColor2G": "0",
        "TeamColor2B": "0",
        "TurfPattern": "0",
        "SidelineColour": "0",
        "SeatColour": "0",
        "GoalStyle": "0",
        "NetPattern": "0",
        "GoalNettingDesign": "1",
        "GoalNettingColor1R": "0",
        "GoalNettingColor1G": "0",
        "GoalNettingColor1B": "0",
        "GoalNettingColor2R": "0",
        "GoalNettingColor2G": "0",
        "GoalNettingColor2B": "0",
        "Sponsor1": "-1",
        "Sponsor2": "-1",
        "Sponsor3": "-1",
        "SponsorFile1": "",
        "SponsorFile2": "",
        "SponsorFile3": "",
        "SponsorColorR": "0",
        "SponsorColorG": "0",
        "SponsorColorB": "0",
        "EditName": "False",
        "EditEmblem": "False",
        "EditStadium": "False",
        "EditStadiumName": "False",
        "EditStadiumFile": "False",
        "EditStadiumDetails": "False",
        "EditStadiumDetails2": "False",
        "EditRivals": "False",
        "EditBanners": "False",
        "EditTeamColors": "False",
        "EditCoach": "False",
        "EditSponsorFile": "False",
        "EditSponsorColors": "False",
        "EditSponsor": "False",
        "Edit1": "False",
        "Fake": "False",
        "LicencedPlayers": "True",
        "LicencedKits": "True",
        "LicencedCoach": LicencedCoach,
        "LicencedCoach2": LicencedCoach2,
        "FeederTeam": "0",
        "ParentTeam": "0",
        "NonPlayableLeague": NonPlayableLeague,
        "HasAnthem": HasAnthem,
        "AnthemStandingStyle": AnthemStandingStyle,
        "AnthemPlayersSinging": AnthemPlayersSinging,
        "AnthemStandingAngle": AnthemStandingAngle,
        "Value1": "-1",
        "Value2": "False",
        "Value3": "0",
        "Value4": "0",
        "Value5": "0",
        "Value6": "0",
        "Value7": "-1",
        "ValueFF": "0",
        "Team2020_1": "0",
        "Team2020_2": Team2020_2,
        "Team2020_3": Team2020_3,
        "Team2020_4": Team2020_4,
        "Team2020_5": "0",
        "Team2020_6": Team2020_6,
        "Team2020_7": "0",
        "Team2020_8": "0",
        "Team2020_9": Team2020_9,
        "Team2020_10": Team2020_10,
        "Team2020_11": Team2020_11,
        "Country2020_1": Country2020_1,
        "Country2020_2": Country2020_2,
        "Country2020_3": Country2020_3,
        "Country2020_4": Country2020_4,
        "Country2020_5": Country2020_5,
        "Value2020_1": Value2020_1,
        "Value2020_2": Value2020_2,
        "Value2020_3": Value2020_3,
        "Value2020_4": Value2020_4,
        "Value2020_5": Value2020_5,
        "Value2020_6": Value2020_6,
        "Value2020_7": Value2020_7,
        "Value2020_8": Value2020_8,
        "Value2020_9": Value2020_9,
        "Value2020_10": Value2020_10,
        "Value2020_11": "0",
        "Value2020_12": "0",
        "Value2020_13": "-1",
        "Value2020_14": "0",
        "Value2020_15": "0",
        "Value2020_16": "0",
        "Value2020_17": "0",
    }

    if impbool == True:
        teams_df = pd.concat(
            [teams_df, pd.DataFrame(dict, index=[0])], ignore_index=True
        )
    if impbool == False:
        revise_teams_df = pd.concat(
            [revise_teams_df, pd.DataFrame(dict, index=[0])], ignore_index=True
        )
    print("Team : " + team_name)
    return r


def createReviseTeams():
    revise_teams_df.to_csv("Output/Revise Teams - Bin.csv", index=False, sep=";")


def createTeams():
    teams_df.to_csv("Output/Teams - Bin.csv", index=False, sep=";")
