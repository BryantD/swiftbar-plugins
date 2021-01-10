# wow-quest-tracker

A WoW world quest tracker for [SwiftBar](https://github.com/swiftbar/SwiftBar).

This project is under an MIT license. 

# Requirements

* SwiftBar
* Python 3 (requests, BeautifulSoup)

# Installation

1. Download [wow.2h.py](https://github.com/BryantD/swiftbar-plugins/blob/main/Games/wow.2h.py) to your SwiftBar plugin folder
1. Edit the configure() function to reflect your needs
    * emissaries_flagged is a list of full faction names
    * quests_flagged is a list of substrings to look for in the quest name
    * Other options should be fairly self-evident

# Usage

<img src="https://github.com/BryantD/swiftbar-plugins/blob/main/images/wow-quests-doc-image-01.png" alt="Plugin example" width=400>

A [!] icon shows up in the menu bar if there are any quests which match
your flags; these will also be called out in the dropdown. Click on a 
quest to go to the quest's Wowhead page.

I happened to need to track BfA emissaries and SL world quests, so
that's all this plugin tracks. If you need something else I'll
happily take a pull request.

# Untested

As of 1.0, I haven't tested end of month time calculations.

This probably doesn't work with
[BitBar](https://github.com/matryer/bitbar), only because I use
SwiftBar's SFSymbol support. Easy enough to add, I just haven't
done it.

# Getting Help

You can mail me at my address above, or [file an issue in
GitHub](https://github.com/BryantD/wow-quest-tracker/issues).

