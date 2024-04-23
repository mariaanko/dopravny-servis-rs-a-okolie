#!/bin/bash

echo "starting script"

if [[ -f ../fb_token.sh ]]
then
  source ../fb_token.sh
  chmod +x scraper.py
  nohup python scraper.py > custom-log.log 2>&1 &
else
        print "please create a script '../fb_token.sh' and set a FB_TOKEN variable there"
fi