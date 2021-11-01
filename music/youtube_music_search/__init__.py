# AUTHOR: Noah Broyles
# DESCRIPTION: Uses the YouTube Music search API to find videoURLs, titles, artists, and thumbnail images for any songs searched for. 
#
# Last Working: Oct 25, 2021

import re
import json
import requests

from addict import Dict

# This API does use some form of key, which is automatically borrowed from YouTube ;)
INNERTUBE_API_KEY = 'AIzaSyC9XL3ZjWddXya6X74dJoCTL-WEYFDNX30'


# This is run when the old API key expires
def refresh_api_key():
    global INNERTUBE_API_KEY
    print('Refreshing API key')
    index_page = requests.get('https://music.youtube.com', headers={"user-agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:92.0) Gecko/20100101 Firefox/92.0"})
    html = index_page.content.decode()

    # The exact length of the key as of 10/25/2021 is 39. 4 years ago (https://stackoverflow.com/questions/44614612) it was also 39.
    # So it's safe to assume a length of 39.
    INNERTUBE_API_KEY = re.findall(r'"INNERTUBE_API_KEY":\s*"(.{39})",', html)[0]
    print(f"The new INNERTUBE_API_KEY is {INNERTUBE_API_KEY}")


def search_youtube_music(search_query: str):

    API_HEADERS = {
        "origin": "https://music.youtube.com",
        "referrer": "https://music.youtube.com/",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "same-origin",
        "sec-fetch-site": "same-origin",
        "x-youtube-client-name": "69",
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0,gzip(gfe)"
    }

    request_body = {
        "context": {
            "client": {
            "hl": "en",
            "gl": "US",
            # "remoteHost": "ip address",
            "deviceMake": "",
            "deviceModel": "",
            # "visitorData": "CgtMLXRBY1dfd1BVYyjxv9uLBg%3D%3D",
            "userAgent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0,gzip(gfe)",
            "clientName": "WEB_REMIX",
            "clientVersion": "1.20211018.00.00",
            "osName": "X11",
            "osVersion": "",
            "originalUrl": "https://music.youtube.com/",
            "platform": "DESKTOP",
            "clientFormFactor": "UNKNOWN_FORM_FACTOR",
            # "configInfo": {
            #     "appInstallData": "CPG_24sGEJLVrQUQkdetBRC3y60FELDUrQUQt7v9EhDYvq0F"
            # },
            "browserName": "Firefox",
            "browserVersion": "93.0",
            "userInterfaceTheme": "USER_INTERFACE_THEME_DARK",
            "timeZone": "America/New_York",
            "musicAppInfo": {
                "pwaInstallabilityStatus": "PWA_INSTALLABILITY_STATUS_UNKNOWN",
                "webDisplayMode": "WEB_DISPLAY_MODE_BROWSER",
                "musicActivityMasterSwitch": "MUSIC_ACTIVITY_MASTER_SWITCH_INDETERMINATE",
                "musicLocationMasterSwitch": "MUSIC_LOCATION_MASTER_SWITCH_INDETERMINATE"
            }
            },
            "user": {
            "lockedSafetyMode": True,
            },
            "request": {
                "useSsl": True,
                "internalExperimentFlags": [],
                "consistencyTokenJars": []
            },
        },
        "query": search_query,
        "suggestStats": {
            "validationStatus": "VALID",
            "parameterValidationStatus": "VALID_PARAMETERS",
            "clientName": "youtube-music",
            "searchMethod": "ENTER_KEY",
            "inputMethod": "KEYBOARD",
            "originalQuery": search_query,
            "zeroPrefixEnabled": True
        }
    }

    def _get_api_response():
        return Dict(requests.post(f"https://music.youtube.com/youtubei/v1/search?key={INNERTUBE_API_KEY}", headers=API_HEADERS, data=json.dumps(request_body)).json())
    
    response = _get_api_response()

    while response.error.message == "API key not valid. Please pass a valid API key.":
        refresh_api_key()
        response = _get_api_response()

    videos = Dict()
    
    distinct_videos = [
        v.musicShelfRenderer.contents[0].musicResponsiveListItemRenderer 
        for v in response.contents.tabbedSearchResultsRenderer.tabs[0].tabRenderer.content.sectionListRenderer.contents
        if v.musicShelfRenderer.contents[0].musicResponsiveListItemRenderer.flexColumns[1].musicResponsiveListItemFlexColumnRenderer.text.runs[0].text in ["Song", "Video"]
    ]

    index = 0
    for video in distinct_videos:
        videos[index] = Dict(
            title=video.flexColumns[0].musicResponsiveListItemFlexColumnRenderer.text.runs[0].text,
            artist=video.flexColumns[1].musicResponsiveListItemFlexColumnRenderer.text.runs[2].text,
            length=video.flexColumns[1].musicResponsiveListItemFlexColumnRenderer.text.runs[6].text,
            videoURL=f"https://youtu.be/{video.playlistItemData.videoId}",
            thumbnail=video.thumbnail.musicThumbnailRenderer.thumbnail.thumbnails[0].url
        )
        index += 1

    return videos
