import sys
import vlc
import math
import pafy
import json
import random
import selectors
import tubehelper

from termcolor import colored

print(colored("YOUTUBE MUSIC STREAMER ROARING TO LIFE...", "blue"))

actions = colored("play", "green") + "        > play song from url or search\n" \
          + colored("playls", "green") + "     > play a YouTube or local playlist in order\n" \
          + colored("makepls", "green") + "     > make a new local playlist\n" \
          + colored("editpls", "green") + "     > edit an existing local playlist\n" \
          + colored("exit", "green") + "        > exit the player\n"

# Whip out our JSON data
with open("musicData.json", "r") as f:
    music_data = json.load(f)

# creating vlc media player
instance = vlc.Instance("--no-video")
player = instance.media_player_new()

sel = selectors.DefaultSelector()
sel.register(sys.stdin.fileno(), selectors.EVENT_READ)

song_queue = []


def save_JSON():
    with open("musicData.json", "w") as f:
        f.write(json.dumps(music_data, indent=4))


# TODO: Add an actual main method. Right now it just shuffles from a playlist.
def main():
    while True:
        print()
        print('What would you like to do? ("' + colored('show', "yellow") + '" to show commands): ')
        action = input("youtube-streamer ~ $ ").lower().strip()

        if action == "show":
            print("\n" + actions)

        elif action == "exit":
            sys.exit()

        elif action == "playls":
            local = input("YouTube or local playlist? [Y/l] ").lower()
            if local.startswith("y") or local == "":
                plsurl = input("Enter the YouTube Playlist URL or hit <Enter> to play saved playlists: ")
                saved_playlists = music_data["youtubePlaylists"]
                if plsurl != "":
                    songList = tubehelper.getURLsFromPlaylist(plsurl)
                    saved = False
                    for pls in saved_playlists:
                        if pls["url"] == plsurl:
                            saved = True
                            break
                    if not saved:
                        if not input("Would you like to save this playlist? [Y/n] ").lower() == "n":
                            name = input("What is the name for this playlist? ")
                            music_data["youtubePlaylists"].append({"name": name, "url": plsurl})
                            save_JSON()
                else:
                    # We be tryna play music from a saved youtube playlist
                    # Let's show them the options
                    count = 1
                    print("\nSaved Playlists:")
                    for pls in saved_playlists:
                        print(colored(f"[{count}] ", "green") + colored(pls["name"], "blue"))
                        count += 1
                    print()
                    pls_number = int(input("Enter the playlist number you want to play: "))
                    songList = tubehelper.getURLsFromPlaylist(saved_playlists[pls_number - 1]["url"])

                shuffle = False
                if input("Would you like to play or shuffle? [P/s]: ").lower().startswith("s"):
                    random.shuffle(songList)
                    shuffle = True

                if not plsurl:
                    print(colored(f"{'Shuffling' if shuffle else 'Playing'} YouTube Playlist ", "green") + colored(
                        f"\x1b]8;;{saved_playlists[pls_number - 1]['url']}\a{saved_playlists[pls_number - 1]['name']}\x1b]8;;\a",
                        color="blue"))
                else:
                    print(colored(f"{'Shuffling' if shuffle else 'Playing'} ", "green") + colored(
                        f"\x1b]8;;{plsurl}\aYoutube Playlist\x1b]8;;\a", color="blue") + "...")

                # We be playin' a YouTube PlayList
                while len(songList) > 0 or len(song_queue) > 0:
                    # If there are songs in the queue, play them first.
                    if song_queue:
                        currentSong = song_queue[0]
                        playStream(currentSong)
                        song_queue.remove(currentSong)
                    else:
                        # Otherwise, play from the normal order
                        currentSong = songList[0]
                        playStream(currentSong)
                        songList.remove(currentSong)


def get_pafy_video(url):
    try:
        video = pafy.new(url)
        return video
    except OSError:
        print(colored(
            f"{url} is a song only meant for YouTube Music Premium users, or is otherwise unavailable. Sorry buddy.",
            "red"))
        return 0


def get_song_time(seconds):
    bal = seconds
    minutes = int(str((seconds / 60)).split('.')[0])
    bal -= (minutes * 60)
    s = int(math.floor(bal))
    if len(str(s)) == 1:
        s = '0' + str(s)
    return str(minutes) + ":" + str(s)


def queue(url=None, songTitle=None):
    if url:
        song_queue.append(url)
        song = get_pafy_video(url)
        if not song:
            return
        print(colored(f"Queued {colored(song.title, 'blue')}", "green"))
    if songTitle:
        url = tubehelper.URLFromQuery(songTitle)
        if url is not None:
            song_queue.append(url)
            song = pafy.new(url)
            if not song:
                return
            print(colored(f"Queued {colored(song.title, 'blue')}", "green"))
        else:
            print(colored(f"{songTitle} could not be found. Try again with a different search term.", "red"))


def playStream(url):
    video = get_pafy_video(url)
    if not video:
        return
    print(colored("Playing ", color="green") + colored(
        f"\x1b]8;;{url}\a{video.title}\x1b]8;;\a ({tubehelper.getVideoID(url)})", color="blue") + " --- " + colored(
        get_song_time(video.length), "blue"))
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
                print(colored(get_song_time(player.get_time() / 1000), "blue"))

            elif do == "pause":
                player.pause()

            elif do == "play":
                player.play()

            elif do.startswith("queue") or do.startswith("q"):
                song_to_queue = ''
                if " " not in do:
                    # Gotta ask 'em what they wanna hear
                    try:
                        song_to_queue = input("Enter the name or URL for the song you wish to queue: ").strip()
                    except KeyboardInterrupt:
                        pass
                else:
                    # They told us what to queue already
                    song_to_queue = " ".join(do.split(" ")[1:])
                if song_to_queue.strip().startswith("https://"):
                    # I guess it's a URL my dude
                    queue(url=song_to_queue)
                else:
                    queue(songTitle=song_to_queue)

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
