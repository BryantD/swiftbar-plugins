#!/bin/bash

# the mit license (mit)
#
# Copyright (c) 2022 Bryant Durrell
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

# <bitbar.title>Letterboxd Showdown</bitbar.title>
# <bitbar.version>v1.0.0</bitbar.version>
# <bitbar.author>Bryant Durrell</bitbar.author>
# <bitbar.author.github>bryantd</bitbar.author.github>
# <bitbar.desc>Show the current Letterboxd showdown</bitbar.desc>
# <bitbar.dependencies>bash, htmlq</bitbar.dependencies>
# <bitbar.image></bitbar.image>
# <bitbar.abouturl>https://github.com/bryantd/swiftbar-plugins</bitbar.abouturl>

HTMLQ=$( which htmlq )

if [[ -z $HTMLQ ]]; then
    if [[ -z ${SWIFTBAR+x} ]]; then
        echo "Please install htmlq: https://github.com/mgdm/htmlq"
    else
        echo "Please install htmlq! | href=https://github.com/mgdm/htmlq"
    fi
    exit
fi

TOPIC=$( /usr/bin/curl --silent https://letterboxd.com/showdown/ | $HTMLQ --text  '.current' )
CLEAN_TOPIC=${TOPIC//[^a-zA-Z0-9]/}
if [[ -z $CLEAN_TOPIC ]]; then
    CLEAN_TOPIC=None
    TOPIC=None
fi

if [[ -z ${SWIFTBAR+x} ]]; then
    TOPIC_FILE=$HOME/var/letterboxd-showdown
    mkdir -p $HOME/var
    touch $TOPIC_FILE
    OLD_TOPIC=$( /bin/cat $TOPIC_FILE )
    if [[ "$CLEAN_TOPIC" != "$OLD_TOPIC" ]]; then
        echo "$CLEAN_TOPIC" > $TOPIC_FILE
        NOTIFICATION="display notification \"${TOPIC}\" with title \"Letterboxd Showdown\""
        /usr/bin/osascript -e "$NOTIFICATION"
    fi
else
   echo "Showdown: ${TOPIC} | href=https://letterboxd.com/showdown/" 
fi 



