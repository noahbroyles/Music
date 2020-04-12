# First use:
Before starting, install the project requirements from `requierments.txt`.
```
$ pip3 install -r requirements.txt
```
Also note that it is important(for now) to keep your `mp3` and `pls` files in the same directory as `play.py`.

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
#### Play Options (VLC Version):
Whenever a song is playing, there are 6 commands you can run at the `> ` prompt:
```
time       > shows the time since the song started in mins:secs
pause      > pauses the song
play       > plays the song
stop/skip  > stops the current song/skips to the next song
restart    > restarts the current song from the beginning 
exit       > returns to main prompt - breaks out of current play queue
```
#### Play Options (Android version):
`Ctrl-C` will skip the current song, `Ctrl-Z` to kill the whole program.  

### Shuffle Mode:
To enter shuffle mode, type `shuffle` at the prompt. The player will play all the songs in a random order. To skip a song in shuffle mode, type `skip`.
  
  
### Download:
To enter download mode, enter `download`at the prompt. You will be asked for a YouTube URL to download `mp3` from. The `mp3` file will be placed in the current directory.  
File names are saved in this format: `TitleOfYoutubeVideo.mp3`  
  
### Geturl:
To get a URL to a YouTube video, type `geturl` at the prompt. You can then enter a search phrase which will return a URL. Videos with 'lyrics' in the title are preferred for obvious reasons.  
The program will ask whether you would like to download the `mp3` from that URL, and whether you would like to play it when it downloads. Respond with `yes/no`. 


  