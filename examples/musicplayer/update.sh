#!/bin/bash

URL=http://localhost:2354/v1

push_image()    { curl -T "$1" "$URL/areas/$2"; }
push_text()     { curl -X PUT -d "$1" "$URL/areas/$2"; }
set_time()      { push_text "$(date +%H:%M)" time; }
play()          { push_image bplay.png run; }
pause()         { push_image bpause.png run; }

#push_image sleep.png sleep
push_image bbar.png bar
push_image bvol.png volumebar
push_text "Sound Chaser" songtitle
push_text "Yes - Relayer " artist
play
set_time
while sleep 10
do
	set_time
done
