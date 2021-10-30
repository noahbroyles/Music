import json
import time
import eyed3
import requests

from scraper import CamelCase


def id3_tag_song(song_path: str, song_dict):
    mp3_song = eyed3.load(song_path)

    mp3_song = eyed3.load("song.mp3")
    mp3_song.tag.artist = u"Integrity"
    mp3_song.tag.album = u"Humanity Is The Devil"
    mp3_song.tag.album_artist = u"Integrity"
    mp3_song.tag.title = u"Hollow"
    mp3_song.tag.track_num = 2

    mp3_song.tag.save()


def downloadSong(song_title: str):
    form = {
        "q": song_title,
        "page": 0
    }
    start = time.time()
    res = requests.post("https://myfreemp3juices.cc/api/search.php", data=form)
    api_data = json.loads(res.text.strip('();'))
    end = time.time()
    print(f"Duration of search API request: {round(end - start, 2)} seconds")

    # Log the song search API request data
    with open('SearchAPI.json', 'w') as wf:
        json.dump(api_data, wf, indent=4)

    # print(json.dumps(api_data, indent=4))
    # Find a good download URL
    possible_download_urls = []
    for entry in api_data["response"]:
        # print(entry)
        try:
            possible_download_urls.append(entry["url"])
        except TypeError:
            pass

    for mp3_url in possible_download_urls:
        print(f"Getting mp3 resource from {mp3_url}")
        start = time.time()
        mp3_request = requests.get(mp3_url)
        end = time.time()
        print(f"Getting the mp3 resource took {round(end - start, 2)} seconds")
        if mp3_request.status_code == 200:
            with open(f'{CamelCase(song_title)}.mp3', 'wb') as f:
                f.write(mp3_request.content)
                break


if __name__ == "__main__":
    downloadSong("earth lil dicky")
