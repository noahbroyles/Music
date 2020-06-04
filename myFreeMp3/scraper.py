import re
import time
import requests
from os import path

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.firefox.options import Options as FOptions

browserName = 'chrome'


def wait_until(somepredicate, timeout, period=0.25):
    mustend = time.time() + timeout
    while time.time() < mustend:
        if somepredicate(): return True
        time.sleep(period)
    return False


def CamelCase(string):
    return "".join(word.capitalize() for word in string.split(" "))


def downloadSong(songTitle: str):
    # Create browser
    if browserName == 'firefox':
        options = FOptions()
        options.headless = True
        homeDir = path.expanduser('~')
        browser = webdriver.Firefox(executable_path=f"{homeDir}/.drivers/geckodriver", options=options) if path.exists(f"{homeDir}/.drivers/geckodriver") else webdriver.Firefox(options=options)
        browser.get('https://myfreemp3v.com/')
        actions = ActionChains(browser)
    elif browserName == 'chrome':
        options = ChromeOptions()
        options.add_argument("--headless")
        homeDir = path.expanduser("~")
        browser = webdriver.Chrome(executable_path=f'{homeDir}/.drivers/chromedriver', options=options) if path.exists(f"{homeDir}/.drivers/chromedriver") else webdriver.Chrome(options=options)
        browser.get('https://myfreemp3v.com/')
        actions = ActionChains(browser)

    # Search for song
    searchBar = browser.find_element_by_id('query')
    searchBar.send_keys(songTitle)
    searchButton = browser.find_element_by_xpath("/html/body/div[2]/div[1]/div/span/button")
    actions.click(searchButton).perform()

    # Wait until page loads
    def readyToProceed():
        try:
            _ = browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/li[1]/div/a[3]")
        except NoSuchElementException:
            return False
        return True
    wait_until(readyToProceed, timeout=20)

    # Click download button
    download_link = re.search("(?P<url>https?://[^\s]+)", browser.find_element_by_xpath("/html/body/div[2]/div[2]/div[2]/li[1]/div/a[3]").get_attribute('onclick')).group("url").split("'")[0]
    browser.get(download_link)

    # Get final download link
    downloadLink = re.search("(?P<url>https?://[^\s]+)", browser.find_element_by_xpath("/html/body/div[2]/div/div[2]/button").get_attribute('onclick')).group("url").split("'")[0]
    browser.quit()

    # Download the song and save it
    r = requests.get(downloadLink)
    with open(f'{CamelCase(songTitle)}.mp3', 'wb') as f:
        f.write(r.content)
