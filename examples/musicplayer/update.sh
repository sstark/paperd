#!/bin/zsh

# This script listens for mpd events using the mpc idleloop feature. On a song
# change or play/pause event it will fetch new data from mpd and update paperd.

PAPERD_URL=http://localhost:2354/v1

update()        { curl -sS "$PAPERD_URL/update" >/dev/null; }
push_image()    { curl -sS -T "$1" "$PAPERD_URL/areas/$2" >/dev/null; }
push_text()     { curl -sS -X PUT -d "$1" "$PAPERD_URL/areas/$2" >/dev/null; }
set_time()      { push_text "$(date +%H:%M)" time; }
draw_bar()      { push_image bbar.png bar; push_image bvol.png volumebar; }
play()          { draw_bar; push_image bplay.png run; }
pause()         { draw_bar; push_image bpause.png run; }

draw_bar

coproc mpc idleloop
mpc_pid=$!
TRAPINT() { kill $mpc_pid; exit; }
TRAPTERM() { kill $mpc_pid; exit; }

while true
do
    # all lines of mpc output in an array
    out=(${(f)"$(mpc -f '%artist%\t%album%\t%title%\t[(%date%)]' status)"})
    state="/"
    if [[ $#out == 3 ]]
    then
        songdata=$out[1]
        # split first line by tabs
        song=("${(@s:	:)songdata}")
        artist=$song[1]
        album=$song[2]
        title=$song[3]
        date=$song[4]
        case $out[2] in
            "[playing]"*)
                state=🕩
                print "display play icon"
                play
                ;;
            "[paused]"*)
                state=🕨
                print "display pause icon"
                pause
                ;;
        esac
        push_text "${title}" songtitle
        push_text "${artist} - ${album} ${date}" artist
    fi
    print "${state} ${song}"
    update
    print "waiting for mpd event... (ctrl-c to quit)"
    # wait until the mpc co-process outputs something
    read -ep
done
