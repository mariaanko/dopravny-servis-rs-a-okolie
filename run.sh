#!/bin/bash

echo "starting script"

if [ -f ../fb_token.sh ]
then
        source ../fb_token.sh
else
        print "please create a script '../fb_token.sh' and set a FB_TOKEN variable there"
fi

chmod +x scraper.py
nohup python3 $HOME/take-tie-srandicky-eeeej/scraper.py > scraper_log.log &