#!/bin/sh

date 
SECONDS=0
URL='https://www.adn.com'

wget --tries=1 --output-document=- "$URL" > /dev/null 2>&1

echo "$SECONDS,$?" 

