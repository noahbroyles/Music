import googleapiclient.discovery

from urllib.parse import parse_qs, urlparse


def url_from_query(search):
    youtube = googleapiclient.discovery.build('youtube', 'v3', developerKey="AIzaSyAQNDuoM7xf4TpmY2Y_Z0hIaCyq_a7jMCw")
    request = youtube.search().list(q=search, part='snippet', type='video', maxResults=1)
    response = request.execute()
    return f"https://youtu.be/{response['items'][0]['id']['videoId']}"


def get_urls_from_playlist(pls_url: str) -> list:
    """Gets individual URLs from a YouTube playlist URL"""

    query = parse_qs(urlparse(pls_url).query, keep_blank_values=True)
    playlist_id = query["list"][0]

    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyAQNDuoM7xf4TpmY2Y_Z0hIaCyq_a7jMCw")

    request = youtube.playlistItems().list(
        part="snippet",
        playlistId=playlist_id,
        maxResults=50
    )

    playlist_items = []
    while request is not None:
        response = request.execute()
        playlist_items += response["items"]
        request = youtube.playlistItems().list_next(request, response)

    return [f'https://youtube.com/watch?v={v["snippet"]["resourceId"]["videoId"]}' for v in playlist_items]


def get_video_ID(video_url: str) -> str:
    """Returns the video ID of a youtube video from a URL"""
    try:
        return parse_qs(urlparse(video_url).query)['v'][0]
    except KeyError:
        # The 'v' key isn't there, this could be a youtu.be link
        return video_url.split("/")[3][:11]  # YouTube video IDs are 11 chars

