import os
import re
import sys
import random
import time
import vlc
import ytUrl
import signal
import youtube_dl
from termcolor import colored
from mutagen.mp3 import MP3


def CamelCase(string):
    camelString = ''
    for word in string.split(" "):
        camelString += word.capitalize()
    return camelString


def playSong(path):
    """Plays an mp3 file from a given path"""
    # This is OLD
    # if " " in path:
    #     os.system("play-audio '" + path + "'")
    # else:
    #     os.system("play-audio " + path)

    # This is NEW
    audio = MP3(path)
    duration = audio.info.length + 1  # add one because of the 1000 ms delay below
    player = vlc.MediaPlayer(path)
    player.audio_set_delay(1000)  # This is super sexy! It keeps from playback freezing issues (sometimes)
    player.play()
    startClock = time.time()
    print("Playing " + colored(path[:-len(".mp3")], "green") + "...")
    songNotEnded = True
    while songNotEnded:
        totalTime = time.time() - startClock
        if totalTime > duration:
            player.stop()
            break
        if songNotEnded:
            do = input("> ").lower()
        if do == "pause":
            player.pause()
        elif do == "play":
            player.play()
        elif do == "stop" or do == "skip":
            player.stop()
            break
        elif do == "exit":
            player.stop()
            main()
        elif do == "":
            player.stop()
            break


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
    while True:
        actions = colored("play", "green") + "        > plays downloaded mp3 songs\n" + colored("download",
                                                                                                "green") + "    > downloads mp3 from a YouTube URL\n" + colored(
            "geturl", "green") + "      > gives a YouTube URL from a search\n" + colored("exit",
                                                                                         "green") + "        > exit the player"
        action = input('What would you like to do? ("' + colored('show', "yellow") + '" to show commands): ').lower()

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
                print('Shuffling songs... type "skip" to skip one')
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
                test = action.split(" ")[1]
            except IndexError:
                print(colored("Invalid play command.", "red"))
                main()
            song = action[len("play "):]
            song = CamelCase(song)
            if song.endswith(".mp3"):  # the song is equal to the path
                if os.path.exists(song):
                    playSong(song)
                else:
                    print(colored("Song not found.", "red"))
            else:
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


if __name__ == "__main__":
    try:
        songToPlay = sys.argv[1]
        playSong(songToPlay)
    except IndexError:
        main()
    print()
