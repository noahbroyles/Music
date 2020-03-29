import requests
import sys
from bs4 import BeautifulSoup


def urlFromQuery(query):
    query = query.replace(' ', '+')
    try:
        page = requests.get(f'https://www.youtube.com/results?search_query={query}').text
    except requests.exceptions.ConnectionError:
        print("There was an error connecting to YouTube. Check Internet/Proxy settings.")
        sys.exit()
    soup = BeautifulSoup(page, 'html.parser')
    results = soup.find_all('a', {'class': 'yt-uix-tile-link'})
    if len(results) == 0:
        return None
    else:
        for vid in results:
            if '/watch' in vid['href']:
                url = 'https://www.youtube.com' + vid['href']
    return url


if __name__ == "__main__":
    search = input("What do you want to find a link to on YouTube? ")
    url = urlFromQuery(search)
    if url is not None:
        print(url, "is your url")
