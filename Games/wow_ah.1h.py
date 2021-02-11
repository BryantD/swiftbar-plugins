#!/usr/bin/env PYTHONIOENCODING=UTF-8 /usr/local/bin/python3

# The MIT License (MIT)
#
# Copyright (c) 2021 Bryant Durrell
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

# <bitbar.title>WoW Auction House Tracker</bitbar.title>
# <bitbar.version>v1.0.1</bitbar.version>
# <bitbar.author>Bryant Durrell</bitbar.author>
# <bitbar.author.github>BryantD</bitbar.author.github>
# <bitbar.desc>Tracking specific AH items</bitbar.desc>
# <bitbar.dependencies>python3, python-blizzardapi</bitbar.dependencies>
# <bitbar.image></bitbar.image>
# <bitbar.abouturl>https://github.com/BryantD/swiftbar-plugins</bitbar.abouturl>

from blizzardapi import BlizzardApi
import os, sys
import configparser


def get_config(config_name):
    sb_plugin_dir = os.getenv("SWIFTBAR_PLUGINS_PATH")
    real_plugin_path = os.getenv("SWIFTBAR_PLUGIN_PATH") or sys.argv[0]
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


def main():
    config = get_config("wow_ah.ini")

    if config:
        api_client_id = (
            config["API"]["client_id"]
            if config.has_option("API", "client_id")
            else False
        )
        api_secret = (
            config["API"]["secret"] if config.has_option("API", "secret") else False
        )
        connected_realm_id = (
            config["Server"]["connected_realm_id"]
            if config.has_option("Server", "connected_realm_id")
            else False
        )
        
        if not (api_client_id and api_secret and connected_realm_id):
            print(f"WoW AH: error in config file")
            sys.exit()

        target_item_id = int(config["Item"]["item_id"])
        if config.has_option("Item", "context"):
            target_item_context = int(config["Item"]["context"])
        else:
            target_item_context = False
        target_item_name = config["Item"]["item_name"]

        api_client = BlizzardApi(api_client_id, api_secret)

        buyout_list = []

        auction_data = api_client.wow.game_data.get_auctions(
            "us", "en_US", connected_realm_id
        )
        for item in auction_data["auctions"]:  # context doesn't exist for most auctions
            if (
                item["item"]["id"] == target_item_id
            ):  # This could be collapsed down but would be less readable
                if target_item_context:
                    if item["item"]["context"] == target_item_context:
                        buyout_list.append(int(item["buyout"] / 10000))
                else:
                    buyout_list.append(int(item["buyout"] / 10000))

        buyout_list.sort(reverse=True)
        if len(buyout_list) > 0:
            print(f"{target_item_name}: {buyout_list[0]:,}G")
        else:
            print(f"{target_item_name}: none found")
    else:
        print("WoW AH: config file not found")


if __name__ == "__main__":
    main()
