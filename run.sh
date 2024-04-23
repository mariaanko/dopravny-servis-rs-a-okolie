#!/bin/bash

echo "starting script"

if [ -f ../fb_token.sh ]
then
        source ../fb_token.sh
else
        print "please create a script '../fb_token.sh' and set a FB_TOKEN variable there"
fi
nohup /home/traffic/take-tie-srandicky-eeeej/scraper.py > custom-output.log