# Bryant's SwiftBar Plugins

This repo contains various [SwiftBar](https://github.com/swiftbar/SwiftBar) plugins 
I've written. They are not compatible with BitBar, because I take advantage of 
SwiftBar features (environment variables, SF Symbols).

All plugins are released under an MIT license.

## drivethrurpg-deal-day

Displays the current Deal of the Day at [DriveThruRPG](https://www.drivethrurpg.com/).

### Requirements

* Python 3 (requests, BeautifulSoup)

### Installation 

1. Download [drivethrurpg-deal-day.1d.py](https://github.com/BryantD/swiftbar-plugins/blob/main/Games/drivethrurpg-deal-day.1d.py) to your SwiftBar

### Usage

The item name and price displays in the menu bar. The drop down menu contains a list of 
rules systems the item works with. Click any rules system to go to the item page.

## wow-quest

A WoW world quest tracker.

### Requirements

* Python 3 (requests, BeautifulSoup)

### Installation

1. Download [wow-quest.2h.py](https://github.com/BryantD/swiftbar-plugins/blob/main/Games/wow-quest.2h.py) to your SwiftBar plugin folder
1. Edit the configure() function to reflect your needs
    * emissaries_flagged is a list of full faction names
    * quests_flagged is a list of substrings to look for in the quest name
    * Other options should be fairly self-evident

### Usage

<img src="https://github.com/BryantD/swiftbar-plugins/blob/main/images/wow-quests-doc-image-01.png" alt="Plugin example" width=400>

A [!] icon shows up in the menu bar if there are any quests which match
your flags; these will also be called out in the dropdown. Click on a 
quest to go to the quest's Wowhead page.

I happened to need to track BfA emissaries and SL world quests, so
that's all this plugin tracks. If you need something else I'll
happily take a pull request.

## wow-ah

A very simple WoW auction house tracker. Unfortunately it currently requires some
persistence to get it working.

### Requirements

* Python 3 (python-blizzardapi)

### Installation

1. Download [wow-ah.1h.py](https://github.com/BryantD/swiftbar-plugins/blob/main/Games/wow-ah.1h.py) to your SwiftBar plugin folder
1. Generate a set of Blizzard API tokens [here](https://develop.battle.net/access/clients) (you must have a Blizzard account)
1. Create a ``config`` folder inside your SwiftBar plugin folder
1. Create a file in your ``config`` folder called ``wow_ah.ini``
1. Add the API tokens and item information to that file, following the pattern here:

    [API]  
    client_id=<created in step two>  
    secret=<created in step two>  

    [Server]
    connected_realm_id=<realm ID>

    [Item]  
    item_name=<free form text, doesn't need to be the actual item name>  
    item_id=<WoW item ID>  
    context=<ID for the specific variant of an item (runecrafted base items have this)>  

To find a realm ID, log into a character on the desired server and paste this 
string into chat:

	/run local x=GetRealmID(); print("Realm ID: ", x)

To find an item_id, check [Wowhead](https://www.wowhead.com). The item ID is in the URL for any item page.

The context is optional; you don't need it unless you're looking for a specific 
variant of a multi-variant item. You can find the context number for an item via
the WoW Auction House API. There is no documentation for this. I'll play with it more
at some point and hopefully write better docs.

### Usage

Really simple: you'll get a menu bar that shows the item name you specified and
the price in gold. Silver and copper is rounded off.

## Getting Help

You can email me at durrell@innocence.com, or [file an issue in
GitHub](https://github.com/BryantD/swiftbar-plugins/issues).

