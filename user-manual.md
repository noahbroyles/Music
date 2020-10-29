# First use:
Before starting, install the project requirements from `requierments.txt`.
```commandline
$ pip3 install -r requirements.txt
```
Also note that there is a `MUSIC_DIRECTORY` variable on line 14 which defaults to `os.curdir`. You can change this to wherever you keep your music, and the music player will play songs out of that directory. 
If you would like to use my provided songs and playlists(which I highly recommend), run this pro command(_Linux and Mac Only_):
```commandline
$ mv songs/* . && rm -fr songs
```
This will move some songs and playlists into the main project directory, which is great. That means you can get right to the 🎵🎵🎵.
## Basic Use:
To start the program, run:
```commandline
$ python3 music
```
This runs the whole `music` Python module, instead of just a Python _file_ like people normally do. Why? Because I felt like doing it that way.
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
#### Play Options:
Whenever a song is playing, there are 6 commands you can run at the `> ` prompt:
```
time       > shows the time since the song started in mins:secs
pause      > pauses the song
play       > plays the song
stop/skip  > stops the current song/skips to the next song
restart    > replays the current song from the beginning 
exit       > returns to main prompt - breaks out of current play queue
```

### Shuffle Mode:
To enter shuffle mode, type `shuffle` at the prompt. The player will play all the songs in a random order. To skip a song in shuffle mode, type `skip`.
  
### Download from URL:
To enter download mode, enter `download`at the prompt. You will be asked for a YouTube URL to download `mp3` from. The `mp3` file will be placed in the current directory.  
File names are saved in this format: `TitleOfYoutubeVideo.mp3`  
  
### Get a URL:
To get a URL to a YouTube video, type `geturl` at the prompt. You can then enter a search phrase which will return a URL. Videos with 'lyrics' in the title are preferred for obvious reasons.  
The program will ask whether you would like to download the `mp3` from that URL, and whether you would like to play it when it downloads. Respond with `yes/no`. 

### Play a Playlist:
To play a playlist, enter `playls` at the prompt. You will be shown a list of all `pls` files in the same directory with a number associated with them. To play one, enter the playlist number.  To exit from here, enter `0`.  
  
### Make a Playlist:
To create a playlist, enter `makepls` at the prompt. You will be asked for a playlist name. The format for these names is `CamelCase`. If you enter a name with spaces in it, it will `CamelCased` for you.😉  
The program will print a list of songs with a number associated with each one. Enter a song number to add it to the playlist. When you are done adding songs, type `stop`. You will be prompted to save the playlist. Enter `yes/no`.  
  
### Edit a Playlist:
To edit an existing playlist... Well, use `editpls`. You will be shown a list of playlists to edit - they are all numbered. Pick one. You'll be shown a list of all songs(with numbers) and the current songs in the playlist.    
As you go through the songs in the playlist, enter a new song number to *replace* the current song, just hit `<enter>` to *keep* it, `del` to just *remove* it, or `stop` when you're satisfied with your new playlist. You'll then be asked to save it or not. You should probably say `yes/no`.  
  
  
# Troubleshooting:
![too bad.](https://camo.githubusercontent.com/df781f87da2f2db87b5cc3125d5459bc70812112/687474703a2f2f64726f70732e6b796c65666f782e63612f31637147502b) <br>
_Read the da*n code and make a Pull Request._ Thanks.
 
 
  
 
  
