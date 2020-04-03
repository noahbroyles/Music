from youtube_search import YoutubeSearch
import json


def urlFromQuery(query):
    results = YoutubeSearch(query, max_results=4).to_json()
    data = json.loads(results)
    results = data['videos']
    videos = [v for v in results]
    for vid in videos:
        if "lyric" in vid['title'].lower():
            url = "https://www.youtube.com" + vid["link"]
            return url
    return "https://www.youtube.com" + videos[0]["link"]


if __name__ == "__main__":
    search = input("What do you want to find a link to on YouTube? ")
    url = urlFromQuery(search)
    if url is not None:
        print(url, "is your url")
