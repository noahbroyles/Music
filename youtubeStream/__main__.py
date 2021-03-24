
import vlc
import pafy
import time
import random
import tubeParser
from termcolor import colored

print(colored("YOUTUBE MUSIC STREAMER ROARING TO LIFE...", "blue"))

# creating vlc media player
instance = vlc.Instance("--no-video")
player = instance.media_player_new()

psUrl = "https://www.youtube.com/watch?v=UQ8cXH7qbVU&list=PLHNntV_whvgol2o__jwedNtjVJSdQQFhD"
songs = tubeParser.getURLsFromPlaylist(psUrl)
random.shuffle(songs)

for song in songs:
    try:
        video = pafy.new(song)
        print(colored("Playing ", color="green") + colored(f"\x1b]8;;{song}\a{video.title}\x1b]8;;\a ({tubeParser.getVideoID(song)})", color="blue"))
        best = video.getbest()

        media = instance.media_new(best.url)
        player.set_media(media)

        # start playing video
        player.play()

        while player.get_state() != vlc.State.Ended:
            time.sleep(0.7)
    except KeyboardInterrupt:
        player.stop()
    songs.remove(song)
    del media
