#!/usr/bin/env pythonioencoding=utf-8 /usr/local/bin/python3

# the mit license (mit)
#
# copyright (c) 2021 bryant durrell
#
# permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "software"), to deal
# in the software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the software, and to permit persons to whom the software is
# furnished to do so, subject to the following conditions:
#
# the above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the software.
#
# the software is provided "as is", without warranty of any kind, express or
# implied, including but not limited to the warranties of merchantability,
# fitness for a particular purpose and noninfringement. in no event shall the
# authors or copyright holders be liable for any claim, damages or other
# liability, whether in an action of contract, tort or otherwise, arising from,
# out of or in connection with the software or the use or other dealings in the
# software.

# <bitbar.title>cagematch last show</bitbar.title>
# <bitbar.version>v1.0.0</bitbar.version>
# <bitbar.author>bryant durrell</bitbar.author>
# <bitbar.author.github>bryantd</bitbar.author.github>
# <bitbar.desc>show the last show w/ratings from specific promotion</bitbar.desc>
# <bitbar.dependencies>python3, beautifulsoup</bitbar.dependencies>
# <bitbar.image></bitbar.image>
# <bitbar.abouturl>https://github.com/bryantd/swiftbar-plugins</bitbar.abouturl>

from bs4 import BeautifulSoup
import requests
import configparser
import datetime
from string import Template
import os, sys


def get_config(config_name):

    sb_plugin_dir = os.getenv("swiftbar_plugins_path")
    real_plugin_path = os.getenv("swiftbar_plugin_path") or sys.argv[0]
    real_plugin_dir = os.path.dirname(real_plugin_path)

    if os.path.isfile(f"{sb_plugin_dir}/config/{config_name}"):
        config_path = f"{sb_plugin_dir}/config/{config_name}"
    elif os.path.isfile(f"{real_plugin_dir}/config/{config_name}"):
        config_path = f"{real_plugin_dir}/config/{config_name}"
    else:
        return False

    config = configparser.ConfigParser()
    config.read(config_path)
    return config


def get_promotion_id(events_url, promotion):
    try:
        req = requests.get(events_url, headers={"accept-encoding": "identity"})
    except requests.exceptions.requestexception as e:
        raise systemexit(e)

    soup = BeautifulSoup(req.text, "html.parser")

    promo_dropdown = soup.find("select", attrs={"name": "sPromotion"})
    options = promo_dropdown.find_all("option")

    for option in options:
        if option.text == promotion:
            return option["value"]

    return false


def get_event_list(event_list_url, promotion_id):
    event_list = []
    event_list_url_template = Template(event_list_url)
    date_to = datetime.date.today()
    date_from = date_to - datetime.timedelta(days=30)

    try:
        req = requests.get(
            event_list_url_template.substitute(
                id=promotion_id,
                day_from=date_from.day,
                month_from=date_from.month,
                year_from=date_from.year,
                day_to=date_to.day,
                month_to=date_to.month,
                year_to=date_to.year,
            ),
            headers={"accept-encoding": "identity"},
        )
    except requests.exceptions.requestexception as e:
        raise systemexit(e)

    soup = BeautifulSoup(req.text, "html.parser")

    event_table = soup.find("table", class_="TBase").find_all(
        "tr", class_=["TRow1", "TRow2"]
    )

    for e in event_table:
        event_date = datetime.date(
            int(e.select("td")[1].text.split(".")[2]),
            int(e.select("td")[1].text.split(".")[1]),
            int(e.select("td")[1].text.split(".")[0]),
        )
        event_name = e.select("td")[2].text.strip()
        event_name = event_name.replace("Tag ", "Day ", 1)
        # Imperfect hack, since some events will have "Tag" in the name
        event_url = e.select("td")[2].select("a")[1]["href"]
        event_id = event_url.split("=")[-1]
        # lazy, could break if format changes
        event_rating = (
            e.select("td")[6].find("span").text
            if e.select("td")[6].find("span")
            else ""
        )
        event_list.append(
            {
                "date": event_date,
                "name": event_name,
                "id": event_id,
                "rating": event_rating,
                "url": "https://cagematch.net/" + event_url + "&page=3",
            }
        )

    return event_list


def get_event_matches(event_url, event_id):
    match_list = []
    event_url_template = Template(event_url)
    try:
        req = requests.get(
            event_url_template.substitute(id=event_id),
            headers={"accept-encoding": "identity"},
        )

    except requests.exceptions.requestexception as e:
        raise systemexit(e)

    soup = BeautifulSoup(req.text, "html.parser")
    match_list_div = soup.find("div", class_="Matches")
    for match in match_list_div.find_all(class_="Match"):
        match_type = match.find("div", class_="MatchType").text
        match_wrestlers = match.find("div", class_="MatchResults").text
        match_rating = (
            match.find("div", class_="MatchRecommendedLine").text
            if match.find("div", class_="MatchRecommendedLine")
            else ""
        )
        match_rating = match_rating[
            match_rating.find(":::: Matchguide Rating: ")
            + 24 : match_rating.find(" based on")
        ]
        # match_won_rating = (
        # 	 match.select("span", class_="MatchRecommendedWON").text
        # 	 if match.select("span", class_="MatchRecommendedWON")
        # 	 else ""
        # )
        match_won_rating = ""

        match_list.append(
            {
                "type": match_type,
                "wrestlers": match_wrestlers,
                "rating": match_rating,
                "won_rating": match_won_rating,
            }
        )

    return match_list


def show_match_data(event, matches):
    parsed_event_rating = f'({event["rating"]})' if event["rating"] else ""
    print(f'{event["name"]}: {event["date"].__format__("%x")} {parsed_event_rating}')
    print("---")
    for match in matches:
        parsed_match_rating = f'({match["rating"]})' if match["rating"] else ""
        print(
            f'{match["type"]}: {match["wrestlers"]} {parsed_match_rating} |href={event["url"]}'
        )
    return

    # [{'type': 'G1 Climax 2021 Block B Match', 'wrestlers': 'Hiroshi Tanahashi vs. Kazuchika Okada', 'rating': '9.03', 'won_rating': ''}]


def main():
    config = get_config("cagematch-shows.ini")

    if config:
        promotion = (
            config["Config"]["promotion"]
            if config.has_option("Config", "promotion")
            else "New Japan Pro Wrestling"
        )
        promotion_id = (
			config["Config"]["promotion_id"]
            if config.has_option("Config", "promotion_id")
            else False
        )

    else:
        promotion = "New Japan Pro Wrestling"
        promotion_id = 7

    promotion_url = "https://www.cagematch.net/?id=1&view=search&sPromotion=$id&sDateFromDay=$day_from&sDateFromMonth=$month_from&sDateFromYear=$year_from&sDateTillDay=$day_to&sDateTillMonth=$month_to&sDateTillYear=$year_to"
    event_list_url = "https://www.cagematch.net/?id=1&view=search"
    event_url = "https://www.cagematch.net/?id=1&nr=$id&page=3"

    if not promotion_id:
        promotion_id = get_promotion_id(event_list_url, promotion)
    if promotion_id:
        events = get_event_list(promotion_url, promotion_id)
        matches = get_event_matches(event_url, events[0]["id"])
        show_match_data(events[0], matches)
    else:
        print(f"Promotion {promotion} not found.")


if __name__ == "__main__":
    main()
