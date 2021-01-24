#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3

# The MIT License (MIT)
#
# Copyright (c) 2020-2021 Bryant Durrell
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# <bitbar.title>WoW Quest Tracker</bitbar.title>
# <bitbar.version>v1.1.1</bitbar.version>
# <bitbar.author>Bryant Durrell</bitbar.author>
# <bitbar.author.github>BryantD</bitbar.author.github>
# <bitbar.desc>Tracking interesting WoW World Quests</bitbar.desc>
# <bitbar.dependencies>python3, requests, beautifulsoup</bitbar.dependencies>
# <bitbar.image>https://github.com/BryantD/swiftbar-plugins/raw/main/images/wow-quests-doc-image-01.png</bitbar.image>
# <bitbar.abouturl>https://github.com/BryantD/swiftbar-plugins</bitbar.abouturl>

import time, datetime, calendar
import os
import json
import requests
from operator import itemgetter
from bs4 import BeautifulSoup


def configure():
    conf = {}

    # Realm
    # Only works for US and EU, since we're scraping Wowhead and that's all they have
    conf["realm"] = "US"

    # Base URLs
    conf["wowhead"] = "https://www.wowhead.com/"
    conf["wowhead_sl_quests"] = "https://www.wowhead.com/world-quests/sl/"
    if conf["realm"] == "US":
        conf["wowhead_sl_quests"] += "na"
    elif conf["realm"] == "EU":
        conf["wowhead_sl_quests"] += "eu"
    conf["wowhead_quest"] = "https://www.wowhead.com/quest="

    # Filters for things I care about
    conf["factions"] = ["alliance", "both"]
    conf["emissaries_flagged"] = [
        "Proudmoore Admiralty",
        "The Waveblade Ankoan",
    ]
    conf["quests_flagged"] = [
        "Enchanting", 
        "Jewelcrafting",
    ]

    # Quest types we care about
    conf["world_quest_types"] = [None, 1, 2]

    # Reference for quest types:
    # null = Maw
    # 0 = Special
    # 1 = Crafting
    # 2 = Vanilla
    # 4 = Pets
    # 15 = Callings

    # UI
    conf["header_color"] = "darkgreen"
    if int(os.environ["OS_VERSION_MAJOR"]) >= 11:
        conf["menu_bar_flag"] = ":exclamationmark.square:"
        conf["quest_flag"] = ":chevron.forward.circle.fill:"
    else:
        conf["menu_bar_flag"] = "[!]"
        conf["quest_flag"] = ">>"
    
    # Miscellanea
    conf[
        "user_agent"
    ] = "Mozilla/5.0 (Macintosh; Intel Mac OS X 11_1) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.2 Safari/605.1.15"

    # Debugging
    conf["debug"] = False
    conf["debug_base"] = ""
    conf["debug_sl_quests"] = ""

    return conf


def show_error(status_code, error):
    print(f"Error {status_code}")
    print(f"--{error} | color=black")


def show_menubar(alert, conf):
    if alert:
        flagged = conf["menu_bar_flag"] 
    else:
        flagged = ""

    print(f"{flagged} WoW")
    print("---")
    return


def get_emissaries(conf):
    emissaries = []
    quest_div_attrs = {"class": "tiw-line-name", "data-side": conf["factions"]}

    if conf["debug"]:
        with open(conf["debug_base"]) as f:
            wowhead_html = f.read()
            f.close
        status_code = 200
    else:
        try:
            r = requests.get(
                conf["wowhead"], headers={"User-Agent": conf["user_agent"]}
            )
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return r.status_code, e
        except requests.exceptions.RequestException as e:
            return -1, e
        status_code = r.status_code
        if status_code == 200:
            wowhead_html = r.text

    soup = BeautifulSoup(wowhead_html, features="html.parser")

    emissary_div = soup.find(id=f'{conf["realm"]}-group-emissary7')
    for quest_div in emissary_div.find_all(attrs=quest_div_attrs):
        emissary_expires_raw = (
            quest_div.previous_sibling.previous_sibling.previous_sibling.previous_sibling.string
        )
        if emissary_expires_raw[-1:] == "h":
            emissary_expires = "today"
        elif emissary_expires_raw == "1d":
            emissary_expires = "tomorrow"
        else:
            emissary_expires = "in two days"
        emissaries.append(
            [
                quest_div.a["href"][7:],
                quest_div.img["alt"][:-5],
                emissary_expires,
                False,
            ]
        )

    return status_code, emissaries


def flag_emissary(emissary, emissary_flag_list):
    if emissary in emissary_flag_list:
        return True
    else:
        return False


def flag_quest(quest, quest_flag_list):
    for flag in quest_flag_list:
        if flag in quest:
            return True

    return False


def show_emissary_header(conf):
    print(f"BfA Emissaries | color={conf['header_color']}")


def show_emissaries(emissaries, conf):
    for emissary in emissaries:
        flagged = conf["quest_flag"] if emissary[3] else ""
        print(
            f'{flagged} {emissary[1]}: expires {emissary[2]} | href={conf["wowhead_quest"]}{emissary[0]}'
        )


def get_single_quest(quest_id, quest_list):
    quest = next(
        quest_data for quest_data in quest_list if quest_data["id"] == int(quest_id)
    )
    return [quest["ending"], quest["worldquesttype"]]


def get_world_quests(conf):
    world_quests = []
    if conf["debug"]:
        with open(conf["debug_sl_quests"]) as f:
            wowhead_quests_html = f.read()
            f.close
        status_code = 200
    else:
        try:
            r = requests.get(
                conf["wowhead_sl_quests"], headers={"User-Agent": conf["user_agent"]}
            )
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            return r.status_code, e
        except requests.exceptions.RequestException as e:
            return -1, e
        status_code = r.status_code
        if status_code == 200:
            wowhead_quests_html = r.text

    soup = BeautifulSoup(wowhead_quests_html, features="html.parser")
    quest_base = soup.find("div", id="list").next_sibling.next_sibling
    quest_json_string = quest_base.string.splitlines()[2]
    quest_json = json.loads(quest_json_string[quest_json_string.index("{") : -2])

    quest_metadata_base = quest_base.next_sibling.next_sibling
    quest_metadata_string = quest_metadata_base.string
    quest_metadata_json = json.loads(
        quest_metadata_string[quest_metadata_string.index("{") : -3]
    )

    for quest_id in quest_json.keys():
        quest_metadata = get_single_quest(quest_id, quest_metadata_json["data"])
        if quest_metadata[1] in conf["world_quest_types"]:
            quest_expires = int(quest_metadata[0] / 1000)
            world_quests.append(
                [
                    quest_id,
                    quest_json[quest_id]["name_enus"],
                    quest_expires,
                    quest_metadata[1],
                    False,
                ]
            )

    return status_code, world_quests


def show_world_quest_header(conf):
    print(f"SL World Quests | color={conf['header_color']}")


def show_world_quests(quests, conf):
    now = time.localtime()

    for quest in quests:
        flagged = conf["quest_flag"] if quest[4] else ""

        expires_time = time.localtime(quest[2])
        expires_string = time.strftime("%I %p", expires_time).lstrip("0")

        day_delta = expires_time[2] - now[2]  # [2] is day of the month
        if expires_time[1] != now[1]:  # [1] is month
            day_delta += calendar.monthrange(now[0], now[1])[1]

        if day_delta == 1:
            expires_string += " tomorrow"
        elif day_delta == 2:
            expires_string += " in two days"
        elif day_delta == 3:
            expires_string += " in three days"

        print(
            f'{flagged} {quest[1]}: expires at {expires_string} | href={conf["wowhead_quest"]}{quest[0]}'
        )


def main():
    conf = configure()
    alert = False

    emissary_status, emissary_data = get_emissaries(conf)

    if emissary_status == 200:
        for emissary in emissary_data:
            if flag_emissary(emissary[1], conf["emissaries_flagged"]):
                emissary[3] = True
                alert = True

    quest_status, quest_data = get_world_quests(conf)

    if quest_status == 200:
        for quest in quest_data:
            if flag_quest(quest[1], conf["quests_flagged"]):
                quest[4] = True
                alert = True

    show_menubar(alert, conf)

    show_emissary_header(conf)
    if emissary_status == 200:
        show_emissaries(emissary_data, conf)
    else:
        show_error(emissary_status, emissary_data)

    print(f"---")

    show_world_quest_header(conf)
    if quest_status == 200:
        show_world_quests(quest_data, conf)
    else:
        show_error(quest_status, quest_data)


if __name__ == "__main__":
    main()
