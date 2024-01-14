from urllib import response
from bs4 import BeautifulSoup as bs
from check_acl_id import checkACLID


def cup_id_scrapper(league_id):
    # ENGLAND
    if league_id == 9 or league_id == 66:
        return 15
    # ITALY
    elif league_id == 10 or league_id == 69:
        return 16
    # SPAIN
    elif league_id == 11 or league_id == 67:
        return 17
    # FRANCE
    elif league_id == 12 or league_id == 68:
        return 18
    # BRAZIL
    elif league_id == 21 or league_id == 90:
        return 24
    # DENMARK
    elif league_id == 128:
        return 129
    # CHILE
    elif league_id == 23:
        return 56
    # COLOMBIA
    elif league_id == 122:
        return 123
    # NETHERLANDS
    elif league_id == 13:
        return 19
    # PAS
    elif league_id == 41:
        return 44
    # BELGIUM
    elif league_id == 111:
        return 112
    # SCOTLAND
    elif league_id == 137:
        return 138
    # PORTUGAL
    elif league_id == 14:
        return 20
    # PLA
    elif league_id == 40:
        return 43
    # SWITZERLAND
    elif league_id == 117:
        return 118
    # TURKEY
    elif league_id == 119:
        return 120
    # ARGENTINA
    elif league_id == 22:
        return 49
    # THAILAND
    elif league_id == 139:
        return 140
    else:
        return 0


def league_info_scrapper(r: response, needed):
    league_ids = []
    league_names = []
    league_urls = []

    soup = bs(r.content, "html.parser")

    for position, league_name_div in enumerate(
        soup.find_all("div", attrs={"class": "team-block-container"})
    ):
        if position == 2 or position == 1:
            if needed == "name":
                for league_name in league_name_div.find_all(
                    "span", attrs={"class": "team-block-name"}
                ):
                    league_names.append(league_name.text)
                return league_names
            for league_div in league_name_div.find_all("a"):
                league_url = league_div.get_attribute_list("href")[0]
                if needed == "url":
                    league_urls.append("https://www.pesmaster.com/" + league_url)
                if needed == "id":
                    league_ids.append(
                        str(league_url).split("/league/")[1].split("/")[0]
                    )
    if needed == "url":
        return league_urls
    if needed == "id":
        return league_ids


def league_scrapper(r: response):
    soup = bs(r.content, "html.parser")
    csvlines = []
    for position, team_name_div in enumerate(
        soup.find("div", attrs={"class": "team-block-container"}).find_all(
            "div", attrs={"class": "team-block"}
        )
    ):
        csvlines.append(
            {
                # Id & IdCompetition are set in main script
                "Id": "",
                "IdCompetition": "",
                "IdTeam": checkACLID(
                    str(team_name_div.find("a").get_attribute_list("href"))
                    .split("team/")[1]
                    .split("/")[0]
                ),
                "Position": str(position),
                "Value1": "0",
                "Value2": "0",
            }
        )
    print("Started League: " + soup.find("h1").text.strip())
    return csvlines
