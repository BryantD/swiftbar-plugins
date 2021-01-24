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
# <bitbar.version>v1.0</bitbar.version>
# <bitbar.author>Bryant Durrell</bitbar.author>
# <bitbar.author.github>BryantD</bitbar.author.github>
# <bitbar.desc>Tracking specific AH items</bitbar.desc>
# <bitbar.dependencies>python3, blizzardapi</bitbar.dependencies>
# <bitbar.image></bitbar.image>
# <bitbar.abouturl></bitbar.abouturl>


from blizzardapi import BlizzardApi
import os, sys
import configparser

def main():
	# TODO: split the config stuff into a function to clean up flow 
	sb_plugin_dir = os.getenv('SWIFTBAR_PLUGINS_PATH') 
	real_plugin_path = os.getenv('SWIFTBAR_PLUGIN_PATH') or sys.argv[0]
	real_plugin_dir = os.path.dirname(real_plugin_path)

	if os.path.isfile(f'{sb_plugin_dir}/config/wow_ah.ini'):
		config_path = f'{sb_plugin_dir}/config/wow_ah.ini'
	elif os.path.isfile(f'{real_plugin_dir}/config/wow_ah.ini'):
		config_path = f'{real_plugin_dir}/config/wow_ah.ini'
	else:
		print("WoW AH: No config")
		quit()

	config = configparser.ConfigParser()
	config.read(config_path)
	
	api_client_id = config['API']['client_id']
	api_secret = config['API']['secret']
	target_item_id = int(config['Item']['item_id'])
	target_item_context = int(config['Item']['context'])
	target_item_name = config['Item']['item_name']
		
	api_client = BlizzardApi(api_client_id, api_secret)
	
	buyout_list = []

	auction_data = api_client.wow.game_data.get_auctions("us", "en_US", 100)
	for item in auction_data['auctions']:
		if item['item']['id'] == target_item_id and item['item']['context'] == target_item_context:
			buyout_list.append(int(item['buyout'] / 10000))
			
	buyout_list.sort(reverse=True)
	print(f"{target_item_name}: {buyout_list[0]:,}G")
			
if __name__ == "__main__":
    main()
