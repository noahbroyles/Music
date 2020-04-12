# First use:
Before starting, install the project requierments from `requierments.txt`.
```
$ pip3 install -r requirements.txt
```
Also note that it is important(for now) to keep your mp3 and pls files in the same directory as `play.py`.

## Basic Use:
To start the program, run:
```
$ python3 play.py
```
The program will prompt you to enter a command. The different commands are:
```
play        > play downloaded mp3 songs
shuffle     > shuffle all downloaded mp3 songs
download    > download mp3 from a YouTube URL
geturl      > get a YouTube URL from a search query
exit        > exit the program
playls      > play songs from a playlist file (.pls)
makepls     > make a new playlist
editpls     > edit an existing playlist
```
You can also type `show` to view this list of actions.

### Play Mode:
To enter play mode, type `play` at the prompt. You will be shown a list of all mp3 songs in the same directory with a number associated with them. Entering a `1` here will shuffle all songs, and entering a `0` will exit play mode. Entering a song number will play that song. Optionally, you can type `play <songname>`. If the songname is found, the player will play the song.

### Shuffle Mode:
To enter shuffle mode, type `shuffle` at the prompt. The player will play all the songs in a random order. To skip a song in shuffle mode, type `skip`.
