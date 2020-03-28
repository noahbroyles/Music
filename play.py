import os
import sys
import random
import vlc
import ytUrl
import youtube_dl
from termcolor import colored


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
    player = vlc.MediaPlayer(path)
    player.play()
    print("Playing " + colored(CamelCase(path)[:-len(".mp3")], "green") + "...")
    while True:
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
            sys.exit()


def download(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': u'%(title)s.%(ext)s',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])


def main():
    while True:
        actions = colored("play", "green") + "        > plays downloaded mp3 songs\n" + colored("download",
                                                                                               "green") + "    > searches YouTube and downloads mp3\n" + colored(
            "geturl", "green") + "      > gives a YouTube URL from a search\n" + colored("exit",
                                                                                         "green") + "        > exit the player"
        print("\n" + actions + "\n")
        action = input("What would you like to do? ").lower()

        if action == "exit":
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
                song = action.split(" ")[1]
            except IndexError:
                print("Invalid play command.")
                main()
            if song.endswith(".mp3"):  # the song is equal to the path
                if os.path.exists(song):
                    playSong(song)
                else:
                    print("Song not found.")
            else:
                path = song + ".mp3"
                if os.path.exists(path):
                    playSong(path)
                else:
                    print("Song not found.")

        elif action == "geturl":
            search = input("What are you searching for? ")
            url = ytUrl.urlFromQuery(search)
            print("Your URL is:", url)
            if (input("Would you like to download " + search + "? ")).lower()[0] == 'y':
                download(url)


if __name__ == "__main__":
    try:
        songToPlay = sys.argv[1]
        playSong(songToPlay)
    except IndexError:
        main()
    print()
