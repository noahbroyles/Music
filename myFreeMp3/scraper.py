# Scrapes the myfreemp3 site with selenium to download Mp3 songs.
# Last confirmed working: 9/26/2021 @ 6:46 PM
import time
import requests
from os import path

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.firefox.options import Options as FOptions

browserName = 'chrome'


def wait_until(somepredicate, timeout, period=0.25):
    mustend = time.time() + timeout
    while time.time() < mustend:
        if somepredicate(): return True
        time.sleep(period)
    return False


def CamelCase(string):
    return " ".join(word.capitalize() for word in string.split(" "))


def downloadSong(songTitle: str, save_directory=None):
    # Create browser
    homeDir = path.expanduser('~')
    if browserName == 'firefox':
        options = FOptions()
        options.headless = True
        browser = webdriver.Firefox(executable_path=f"{homeDir}/.drivers/geckodriver", options=options) if path.exists(f"{homeDir}/.drivers/geckodriver") else webdriver.Firefox(options=options)
    elif browserName == 'chrome':
        options = ChromeOptions()
        options.add_argument("--headless")
        browser = webdriver.Chrome(executable_path=f'{homeDir}/.drivers/chromedriver', options=options) if path.exists(f"{homeDir}/.drivers/chromedriver") else webdriver.Chrome(options=options)
    browser.get('https://myfreemp3juices.cc/')

    # Search for song
    searchBar = browser.find_element_by_id('query')
    searchBar.clear()
    searchBar.send_keys(songTitle)
    searchBar.send_keys(Keys.ENTER)
    searchButton = browser.find_element_by_xpath("/html/body/div[2]/div[1]/div/span/button")
    # Click the search button as well as pushing enter
    # for i in range(2):
    # searchButton.click()

    # Wait until page loads
    def readyToProceed():
        try:
            # /html/body/div[2]/div[2]/div[2]/li[1]/a[1]
            searchButton.click()
            _ = browser.find_element_by_xpath('//*[@id="result"]/div[2]/li[1]/a[1]')
        except NoSuchElementException:
            return False
        return True
    wait_until(readyToProceed, timeout=20)

    # Click download button
    songID = browser.find_element_by_xpath('//*[@id="result"]/div[2]/li[1]/a[1]').get_attribute('data-src').split('/')[-1]
    downloadLink = f"https://speed.idmp3s.com/{songID}"
    browser.quit()

    # Download the song and save it
    r = requests.get(downloadLink)
    if not save_directory:
        with open(f'{CamelCase(songTitle)}.mp3', 'wb') as f:
            f.write(r.content)
    else:
        with open(f'{save_directory}/{CamelCase(songTitle)}.mp3', 'wb') as f:
            f.write(r.content)


# Main for testing
if __name__ == "__main__":
    browserName = 'firefox'
    downloadSong('Yeah!')
