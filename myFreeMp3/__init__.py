from . import chrome
from . import firefox


class SongDownloader:
    def __init__(self, browser):
        if browser.lower() == 'chrome':
            self.download = chrome.downloadSong
        elif browser.lower() == 'firefox':
            self.download = firefox.downloadSong
