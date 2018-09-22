#!/bin/bash

URL=http://localhost:2354/v1

push_image()    { curl -T "$1" "$URL/areas/$2"; }
push_text()     { curl -X PUT -d "$1" "$URL/areas/$2"; }
set_time()      { push_text "$(date +%H:%M)" time; }
play()          { push_image play.png run; }
pause()         { push_image pause.png run; }

push_image volumebar.png volumebar
#push_image sleep.png sleep
push_text "Master of Calypso" songtitle
push_text "Walter Gavitt Ferguson" artist
play
set_time
while true
do
	set_time
	sleep 10
done
