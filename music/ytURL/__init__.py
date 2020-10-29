from cyoutube_search import YoutubeSearch
import requests
import sys


def urlFromQuery(query):
    try:
        results = YoutubeSearch(query, max_results=2).to_dict()
    except requests.exceptions.ConnectionError:
        print("There was an error connecting to YouTube. Check Proxy/Internet settings.")
        sys.exit()
    videos = [v for v in results]
    return videos[0]['url']


if __name__ == "__main__":
    search = input("What do you want to find a link to on YouTube? ")
    url = urlFromQuery(search)
    if url is not None:
        print(url, "is your url")
    else:
        print("No such thing was found.")
