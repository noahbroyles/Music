import googleapiclient.discovery
from urllib.parse import parse_qs, urlparse


def getURLsFromPlaylist(playlistUrl: str) -> list:
    """Gets individual URLs from a YouTube playlist URL"""

    query = parse_qs(urlparse(playlistUrl).query, keep_blank_values=True)
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


def getVideoID(videoURL: str) -> str:
    """Returns the video ID of a youtube video from a URL"""
    return parse_qs(urlparse(videoURL).query)['v'][0]

