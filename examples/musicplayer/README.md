
First run paperd from its directory:

    ./paperd.py -c examples/musicplayer/paperd.yml

When it has finished starting, you can run the update script:

    ./update.sh

This will fake a (not very elaborate) music player display. The idea of course
is that the update script is replaced by something else that will read actual
data from a system like Volumio.

