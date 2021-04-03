import math
import selectors
import sys

import vlc
import pafy
import random
import tubehelper
from termcolor import colored

print(colored("YOUTUBE MUSIC STREAMER ROARING TO LIFE...", "blue"))

# creating vlc media player
instance = vlc.Instance("--no-video")
player = instance.media_player_new()

sel = selectors.DefaultSelector()
sel.register(sys.stdin.fileno(), selectors.EVENT_READ)

psUrl = "https://www.youtube.com/playlist?list=PLHNntV_whvgol2o__jwedNtjVJSdQQFhD"
songList = tubehelper.getURLsFromPlaylist(psUrl)
random.shuffle(songList)

songQueue = []


def getPafyVideo(url):
    try:
        video = pafy.new(url)
        return video
    except OSError:
        print(colored(f"{url} is a song only meant for YouTube Music Premium users. Sorry buddy.", "red"))
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
            print(colored(f"{songTitle} could not be found. Tray again with a different search term.", "red"))


# TODO: Add an actual main method. Right it just shuffles from a playlist.
def main():
    pass


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
            do = input().lower()
            if do == "time":
                print(colored(songTime(player.get_time() / 1000), "blue"))
            elif do == "pause":
                player.pause()
            elif do == "play":
                player.play()
            elif do == "queue":
                try:
                    songToQueue = input("Enter the name or URL for the song you wish to queue: ").strip()
                    if songToQueue.strip().startswith("https://"):
                        # I guess it's a URL my dude
                        queue(url=songToQueue)
                    else:
                        queue(songTitle=songToQueue)
                except KeyboardInterrupt:
                    pass
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
