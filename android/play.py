"""
Plays music from mp3 files in the current directory. I use this with termux on my Android phone, that's why this is in
the android folder.
"""

import os
import re
import sys
import random
import ytUrl
import youtube_dl
import math
from termcolor import colored
from mutagen.mp3 import MP3


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
    duration = MP3(path).info.length
    print("Playing " + colored(path[:-len(".mp3")], "green") + " --- " + colored(str(songTime(duration)), "blue"))
    os.system("play-audio '" + path + "'")


def getMeta(url):
    ydl_opts = {}
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        meta = ydl.extract_info(url, download=False)
    return meta


def download(url, play=False):
    title = CamelCase(re.sub(r" ?\([^)]+\)", "", getMeta(url)['title'])).replace(":", "-")
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


def main():
    actions = colored("play", "green") + "        > plays downloaded mp3 songs\n" + colored("shuffle", "green") + "     > shuffles downloaded songs\n" + colored("download",
                                                                                            "green") + "    > downloads mp3 from a YouTube URL\n" + colored(
        "geturl", "green") + "      > gives a YouTube URL from a search\n" + colored("exit",
                                                                                     "green") + "        > exit the player"
    while True:
        action = input('What would you like to do? ("' + colored('show', "yellow") + '" to show commands): ')

        if action == "show":
            print("\n" + actions + "\n")

        elif action == "exit":
            sys.exit()

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

            # Exit if command is 0
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
                song = CamelCase(song)
                songList = [x for x in os.listdir() if x.endswith(".mp3")]
                if len(song) <= 3:
                    print(colored("Song not found.", "red"))
                elif len(song) >= 4:
                    for s in songList:
                        ls = s.lower()[:-len(".mp3")]
                        if song.lower() in ls or song.lower() == ls:
                            playSong(s)
                            main()
                    print(colored("Song not found.", "red"))  # if we're still here, there was no such song

        elif action == "geturl":
            search = input("What are you searching for? ")
            url = ytUrl.urlFromQuery(search)
            if url is not None:
                print("Your URL is:", colored(url, "blue"))
                if (input("Would you like to download " + colored(search, "green") + "? ")).lower()[0] == 'y':
                    if (input("Do you want to play " + colored(search, "green") + " when it downloads? ")).lower():
                        print()
                        download(url, play=True)
                    else:
                        print()
                        download(url)
            else:
                print("A URL for " + search + " was not found.")

        elif action == "download":
            url = input("Enter the URL to download mp3 from: ")
            if (input("Do you want to play the song when it downloads? ")).lower():
                print()
                download(url, play=True)
            else:
                print()
                download(url)

        elif action == "shuffle":
            songNames = [x for x in os.listdir() if x.endswith(".mp3")]
            songNames = sorted(songNames)
            print()
            print('Shuffling songs... type "' + colored('skip', "yellow") + '" to skip one')
            playableSongs = songNames.copy()
            while len(playableSongs) > 0:
                playingSong = random.choice(playableSongs)
                playSong(playingSong)
                playableSongs.remove(playingSong)


if __name__ == "__main__":
    try:
        songToPlay = sys.argv[1]
        playSong(songToPlay)
    except IndexError:
        main()
    print()
