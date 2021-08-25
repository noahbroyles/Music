import json
import requests

from scraper import CamelCase


def downloadSong(song_title: str):
    form = {
        "q": song_title,
        "page": 0
    }

    res = requests.post("https://myfreemp3juices.cc/api/search.php", data=form)
    api_data = json.loads(res.text.strip('();'))
    # with open('SearchAPI.json', 'w') as wf:
    #     json.dump(api_data, wf, indent=4)
    # print(json.dumps(api_data, indent=4))
    possible_download_urls = []
    for entry in api_data["response"]:
        # print(entry)
        try:
            possible_download_urls.append(entry["url"])
        except TypeError:
            pass

    for mp3_url in possible_download_urls:
        mp3_request = requests.get(mp3_url)
        if mp3_request.status_code == 200:
            with open(f'{CamelCase(song_title)}.mp3', 'wb') as f:
                f.write(mp3_request.content)
                break


if __name__ == "__main__":
    downloadSong("yeah! usher")
