import os
import re
import sys
import random
import vlc
import ytUrl
import selectors
import youtube_dl
import math
from termcolor import colored
from mutagen.mp3 import MP3

actions = colored("play", "green") + "        > plays downloaded mp3 songs\n" \
          + colored("shuffle", "green") + "     > shuffles downloaded songs\n" \
          + colored("download", "green") + "    > downloads mp3 from a YouTube URL\n" \
          + colored("geturl", "green") + "      > gives a YouTube URL from a search\n" \
          + colored("exit", "green") + "        > exit the player\n" \
          + colored("playls", "green") + "      > plays songs from a playlist\n" \
          + colored("makepls", "green") + "     > makes a new playlist"


def CamelCase(string):
    camelString = ''
    for word in string.split(" "):
        camelString += word.capitalize()
    return camelString


def songTime(seconds):
    bal = seconds
    minutes = int(str((seconds / 60)).split('.')[0])
    bal -= (minutes * 60)
    s = int(math.floor(bal))
    if len(str(s)) == 1:
        s = '0' + str(s)
    return str(minutes) + ":" + str(s)


def playSong(path):
    """Plays an mp3 file from a given path"""
    player = vlc.MediaPlayer(path)
    duration = MP3(path).info.length
    player.audio_set_delay(1000)  # keeps vlc from playback freezing issues (only sometimes)
    player.play()
    print("Playing " + colored(path[:-len(".mp3")], "green") + " --- " + colored(str(songTime(duration)), "blue"))

    sel = selectors.DefaultSelector()
    sel.register(sys.stdin.fileno(), selectors.EVENT_READ)
    try:
        while True:
            sys.stdout.write('> ')
            sys.stdout.flush()
            # Poll for command input as long as the player hasn't reached the end
            while player.get_state() != vlc.State.Ended:  # It's still running
                if sel.select(0.1):
                    break  # Input available - time to read input, so stop polling
            else:
                print()  # For beauty
                break  # Quit the command handling loop
            do = input().lower()
            if do == "time":
                print(colored(songTime(player.get_time() / 1000), "blue"))
            elif do == "pause":
                player.pause()
            elif do == "play":
                player.play()
            elif do == "stop" or do == "skip":
                player.stop()
                break
            elif do == "restart":
                player.stop()
                playSong(path)
                break
            elif do == "exit":
                player.stop()
                main()
    except EOFError:
        player.stop()
        sys.exit()


def getMeta(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download=False)
    return meta


def download(url, play=False):
    title = CamelCase(re.sub(r" ?\([^)]+\)", "", getMeta(url)['title'])).replace(":", "-").replace(" ", '')
    if title.endswith('.'):
        title = title[:-1]
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': title + '.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    if play:
        playSong(title + '.mp3')


def searchForSong(search):
    url = ytUrl.urlFromQuery(search)
    if url is not None:
        print("Your URL is:", colored(url, "blue"))
        if (input("Would you like to download " + colored(search, "green") + "? ")).lower()[0] == 'y':
            if (input("Do you want to play " + colored(search, "green") + " when it downloads? ")).lower()[0] == "y":
                print()
                download(url, play=True)
            else:
                print()
                download(url)
    else:
        print("A URL for " + search + " was not found.")


def createPlaylist():
    while True:
        playlistName = input("What would you like to name this playlist? ")
        if ' ' in playlistName:
            playlistName = CamelCase(playlistName)
            print("No spaces allowed in playlist name. " + colored(playlistName, 'green') + " will be the name.")
        filename = playlistName + '.pls'
        if os.path.exists(filename):
            if input("A playlist with that name already exits. Would you like to overwrite it? ").lower()[0] == 'y':
                break
        else:
            break
    playlist = []
    allSongs = [x for x in os.listdir() if x.endswith('.mp3')]
    songNames = sorted(allSongs)
    print()
    songID = 1
    for songName in songNames:
        print("[" + str(songID) + "] Add " + colored(songName[:-len(".mp3")], "green"))
        songID += 1
    print()
    print(colored("Select the songs to add: ", "blue"))
    while True:
        action = input('Enter a song number to add, or type ' + colored("stop", "green") + ': ')
        if action == 'stop' or action == '':
            if len(playlist) != 0:
                data = ""
                for song in playlist:
                    data += song + "\n"
                with open(filename, 'w') as plsFile:
                    plsFile.write(data)
                break
            else:
                break
        else:
            playlist.append(allSongs[int(action) - 1])


def shuffleSongs():
    songNames = [x for x in os.listdir() if x.endswith(".mp3")]
    songNames = sorted(songNames)
    print()
    print('Shuffling songs... type "' + colored('skip', "yellow") + '" to skip one')
    playableSongs = songNames.copy()
    while len(playableSongs) > 0:
        playingSong = random.choice(playableSongs)
        playSong(playingSong)
        playableSongs.remove(playingSong)


def playPlaylist(playlist=None):
    if not playlist:
        plists = [x for x in os.listdir() if x.endswith('.pls')]
        playlistNames = sorted(plists)
        pID = 1
        print()
        for playlistName in playlistNames:
            print("[" + str(pID) + "] Play " + colored(playlistName[:-len(".pls")], "green"))
            pID += 1
        action = int(input("Enter the playlist number to play: "))
        playlist = plists[action - 1]
    with open(playlist, 'r') as plsFile:
        songSequence = [line for line in plsFile]
        print(songSequence)
    for song in songSequence:
        print(song)
        playSong(song)


def main():
    while True:
        action = input('What would you like to do? ("' + colored('show', "yellow") + '" to show commands): ')

        if action == "show":
            print("\n" + actions + "\n")

        elif action == "exit":
            sys.exit()

        elif action == 'playls':
            playPlaylist()

        elif action == "play":
            print()
            songNames = [x for x in os.listdir() if x.endswith(".mp3")]
            songNames = sorted(songNames)
            print("Choose an option: ")
            print("[0] " + colored("Exit", "red"))
            print("[1] " + colored("Shuffle All", "magenta"))
            songID = 2
            for songName in songNames:
                print("[" + str(songID) + "] Play " + colored(songName[:-len(".mp3")], "green"))
                songID += 1
            print()
            command = input("Enter action number: ")

            if command.strip() == "1":  # This is a shuffle play mode
                print()
                print('Shuffling songs... type "' + colored('skip', "yellow") + '" to skip one')
                playableSongs = songNames.copy()
                while len(playableSongs) > 0:
                    playingSong = random.choice(playableSongs)
                    playSong(playingSong)
                    playableSongs.remove(playingSong)

            # back to main if command is 0
            elif command.strip() == "0":
                main()

            else:  # we need to play the songID number
                playingSong = songNames[int(command) - 2]
                playSong(playingSong)

        elif action.startswith("play") and len(action) > 4:
            try:
                action.split(" ")[1]
            except IndexError:
                print(colored("Invalid play command.", "red"))
                main()
            song = action[len("play "):]
            if song.endswith(".mp3"):  # the song is equal to the path
                if os.path.exists(song):
                    playSong(song)
                else:
                    print(colored("Song not found.", "red"))
            else:
                capitalSong = CamelCase(song)
                songList = [x for x in os.listdir() if x.endswith(".mp3")]
                if len(capitalSong) <= 3:
                    print(colored("Song not found.", "red"))
                elif len(capitalSong) >= 4:
                    for s in songList:
                        ls = s.lower()[:-len(".mp3")]
                        if capitalSong.lower() in ls or capitalSong.lower() == ls:
                            playSong(s)
                            main()
                    print(colored("Song not found.", "red"))  # if we're still here, there was no such song
                    if input("Would you like to search YouTube for " + colored(song, 'green') + "? ").lower()[0] == 'y':
                        searchForSong(song)

        elif action == "geturl":
            search = input("What are you searching for? ")
            searchForSong(search)

        elif action == "download":
            url = input("Enter the URL to download mp3 from: ")
            if (input("Do you want to play the song when it downloads? ")).lower()[0] == "y":
                print()
                download(url, play=True)
            else:
                print()
                download(url)

        elif action == "shuffle":
            shuffleSongs()

        elif action == "makepls":
            createPlaylist()


if __name__ == "__main__":
    try:
        songToPlay = sys.argv[1]
        playSong(songToPlay)
    except IndexError:
        main()
    print()
