import math
import selectors
import sys

import vlc
import pafy
import json
import random
import tubehelper
from termcolor import colored

print(colored("YOUTUBE MUSIC STREAMER ROARING TO LIFE...", "blue"))


actions = colored("play", "green") + "        > play song from url or search\n" \
          + colored("playls", "green") + "     > play a YouTube or local playlist in order\n" \
          + colored("makepls", "green") + "     > make a new local playlist\n" \
          + colored("editpls", "green") + "     > edit an existing local playlist" \
          + colored("exit", "green") + "        > exit the player\n"

# Whip out our JSON data
with open("musicData.json", "r") as f:
    jason = json.load(f)

# creating vlc media player
instance = vlc.Instance("--no-video")
player = instance.media_player_new()

sel = selectors.DefaultSelector()
sel.register(sys.stdin.fileno(), selectors.EVENT_READ)

songQueue = []

def saveJSON():
    with open("musicData.json", "w") as f:
        f.write(json.dumps(jason, indent=4))

# TODO: Add an actual main method. Right now it just shuffles from a playlist.
def main():
    while True:
        print()
        print('What would you like to do? ("' + colored('show', "yellow") + '" to show commands): ')
        action = input("youtube-streamer ~ $ ")

        if action == "show":
            print("\n" + actions)

        elif action == "playls":
            local = input("YouTube or local playlist? [Y/l] ").lower()
            if local.startswith("y") or local == "":
                psUrl = input("Enter the YouTube Playlist URL or hit <Enter> to play saved playlists: ")
                savedPlaylists = jason["savedYTPLS"]
                if psUrl != "":
                    songList = tubehelper.getURLsFromPlaylist(psUrl)
                    saved = False
                    for pls in savedPlaylists:
                        if pls["url"] == psUrl:
                            saved = True
                            break
                    if not saved:
                        if not input("Would you like to save this playlist? [Y/n] ").lower() == "n":
                            name = input("What is the name for this playlist? ")
                            jason["savedYTPLS"].append({"name": name, "url": psUrl})
                            saveJSON()
                else:
                    # We be tryna play music from a saved youtube playlist
                    # Let's show them the options
                    count = 1
                    print("\nSaved Playlists:")
                    for pls in savedPlaylists:
                        print(colored(f"[{count}] ", "green") + colored(pls["name"], "blue"))
                        count += 1
                    print()
                    plsNumber = int(input("Enter the playlist number you want to play: "))
                    songList = tubehelper.getURLsFromPlaylist(savedPlaylists[plsNumber - 1]["url"])
                    
                shfl = False
                if input("Would you like to play or shuffle? [P/s]: ").lower().startswith("s"):
                    random.shuffle(songList)
                    shfl = True

                if not psUrl:
                    print(colored(f"{'Shuffling' if shfl else 'Playing'} YouTube Playlist ", "green") + colored(f"\x1b]8;;{savedPlaylists[plsNumber-1]['url']}\a{savedPlaylists[plsNumber-1]['name']}\x1b]8;;\a", color="blue"))
                else:
                    print(colored(f"{'Shuffling' if shfl else 'Playing'} ", "green") + colored(f"\x1b]8;;{psUrl}\aYoutube Playlist\x1b]8;;\a", color="blue") + "...")

                # We be playin' a YouTube PlayList
                while len(songList) > 0 or len(songQueue) > 0:
                    # If there are songs in the queue, play them first.
                    if songQueue:
                        currentSong = songQueue[0]
                        playStream(currentSong)
                        songQueue.remove(currentSong)
                    else:
                        # Otherwise, play from the normal order
                        currentSong = songList[0]
                        playStream(currentSong)
                        songList.remove(currentSong)

def getPafyVideo(url):
    try:
        video = pafy.new(url)
        return video
    except OSError:
        print(colored(f"{url} is a song only meant for YouTube Music Premium users, or is otherwise unavailable. Sorry buddy.", "red"))
        return 0


def songTime(seconds):
    bal = seconds
    minutes = int(str((seconds / 60)).split('.')[0])
    bal -= (minutes * 60)
    s = int(math.floor(bal))
    if len(str(s)) == 1:
        s = '0' + str(s)
    return str(minutes) + ":" + str(s)


def queue(url=None, songTitle=None):
    if url:
        songQueue.append(url)
        song = getPafyVideo(url)
        if not song:
            return
        print(colored(f"Queued {colored(song.title, 'blue')}", "green"))
    if songTitle:
        url = tubehelper.URLFromQuery(songTitle)
        if url is not None:
            songQueue.append(url)
            song = pafy.new(url)
            if not song:
                return
            print(colored(f"Queued {colored(song.title, 'blue')}", "green"))
        else:
            print(colored(f"{songTitle} could not be found. Try again with a different search term.", "red"))


def playStream(url):
    video = getPafyVideo(url)
    if not video:
        return
    print(colored("Playing ", color="green") + colored(f"\x1b]8;;{url}\a{video.title}\x1b]8;;\a ({tubehelper.getVideoID(url)})", color="blue") + " --- " + colored(songTime(video.length), "blue"))
    best = video.getbest()

    media = instance.media_new(best.url)
    player.set_media(media)

    # start playing video
    player.play()

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

            do = input().lower().strip()

            if do == "time":
                print(colored(songTime(player.get_time() / 1000), "blue"))

            elif do == "pause":
                player.pause()

            elif do == "play":
                player.play()

            elif do.startswith("queue") or do.startswith("q"):
                if " " not in do:
                    # Gotta ask 'em what they wanna hear
                    try:
                        songToQueue = input("Enter the name or URL for the song you wish to queue: ").strip()
                    except KeyboardInterrupt:
                        pass
                else:
                    # They told us what to queue already
                    songToQueue = " ".join(do.split(" ")[1:])
                if songToQueue.strip().startswith("https://"):
                    # I guess it's a URL my dude
                    queue(url=songToQueue)
                else:
                    queue(songTitle=songToQueue)

            elif do == "stop" or do == "skip":
                player.stop()
                return

            elif do == "exit":
                player.stop()
                del media
                main()

    except EOFError:
        player.stop()
        sys.exit()

if __name__ == "__main__":
    main()