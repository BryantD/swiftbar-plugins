# Bryant's SwiftBar Plugins

This repo contains various [SwiftBar](https://github.com/swiftbar/SwiftBar) plugins 
I've written. They are not compatible with BitBar, because I take advantage of 
SwiftBar features (environment variables, SF Symbols).

All plugins are released under an MIT license.

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

    [Item]  
    item_name=<free form text, doesn't need to be the actual item name>  
    item_id=<WoW item ID -- try WoWhead to find this>  
    context=<kind of a mystery to me>  

I figured out the context number for the item I cared about by manually fiddling
with the WoW Auction House API and discovering that a level 225 Grim-Veiled Hood
always had context=65. There is no documentation for this. I'll play with it more
at some point and hopefully write better docs.

### Usage

Really simple: you'll get a menu bar that shows the item name you specified and
the price in gold. Silver and copper is rounded off.

## Getting Help

You can email me at durrell@innocence.com, or [file an issue in
GitHub](https://github.com/BryantD/swiftbar-plugins/issues).

