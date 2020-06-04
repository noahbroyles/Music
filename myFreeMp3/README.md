# myFreeMp3
_Downloads songs from [MyFreeMp3v.com](https://myfreemp3v.com)_  
## Usage:  
```python
import myFreeMp3

# Create a downloader object using the the chrome selenium driver
cdl = myFreeMp3.SongDownloader('chrome')
# Downloads 'All about that Bass' from the site and saves it as 'All about that Bass.mp3' 
cdl.download('All about that Bass')

# Create a downloader object using the the firefox selenium driver
fdl = myFreeMp3.SongDownloader('firefox')
# Downloads 'All about that Bass' from the site and saves it as 'All about that Bass.mp3' 
fdl.download('All about that Bass')

# The downloader defaults to using chrome
dl = myFreeMp3.SongDownloader() # Uses chrome by default
```
The script will save the song in the same directory as the `myFreeMp3` package, with the exact name of the song you searched for, with `.mp3` extension.   
This program assumes that you have the [`chromedriver`](https://chromedriver.chromium.org/) or [`geckodriver`](https://github.com/mozilla/geckodriver/releases) (for Firefox) in a `.drivers` directory in your home folder, or in your system path.
```
$HOME
|__.drivers
    ├── chromedriver
    └── geckodriver
```
<br>
<sub>You are responsible for any music downloaded in breach of copyright. This is just a tool.</sub>
