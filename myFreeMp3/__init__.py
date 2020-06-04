from . import scraper


class SongDownloader:
    def __init__(self, browser='chrome'):
        scraper.browserName = browser
        self.download = scraper.downloadSong
