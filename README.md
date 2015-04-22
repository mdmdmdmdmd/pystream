# pystream

you can stream your movies with this. yay.
needs flash based flowplayer if you want it embedded.
needs a directory layout of one folder per movie/media, and the media file needs to be directly in that folder.
only tested in python 3.4.2!

TODO:
- make this work with html5 players (the vlc backend is not capable of producing valid streams for this yet it seems)
- make it platform agnostic (currently has some windows-isms like \ instead of /)
- make binding to host and port a config option
- make it more flexible so you dont have to have a specific directory layout
- handle some more errors that currently are still unchecked
