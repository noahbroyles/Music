"""
Plays music from mp3 files in the current directory. I use this with termux on my Android phone, that's why this is in
the android folder.
"""

import sys, os, random
from termcolor import colored

def playSong(path):
    """Plays an mp3 file from a given path"""
    if " " in path:
        os.system("play-audio '" + path + "'")
    else:
        os.system("play-audio " + path)

def main():
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


    if command.strip() == "1": # This is a shuffle play mode
        print()
        print("Shuffling songs... Ctrl-c to skip one")
        playableSongs = songNames.copy()
        while len(playableSongs) > 0:
            playingSong = random.choice(playableSongs)
            print("Now Playing " + colored(playingSong[:-len(".mp3")], "green"))
            try:
                playSong(playingSong)
            except KeyboardInterrupt:
                pass
            playableSongs.remove(playingSong)

    # Exit if command is 0
    elif command.strip() == "0":
        sys.exit()

    else: # we need to play the songID number
            playingSong = songNames[int(command) - 2]
            print("Playing " + colored(playingSong[:-len(".mp3")], "green") + "...")
            playSong(playingSong)



if __name__ == "__main__":
    try:
        try:
            songToPlay = sys.argv[1]
            print("Playing " + colored(songToPlay[:-len(".mp3")], "green") + "...")
            playSong(songToPlay)
        except IndexError:
            main()
    except KeyboardInterrupt:
        sys.exit()
    print()