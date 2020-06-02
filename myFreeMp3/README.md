# myFreeMp3
_Downloads songs from [MyFreeMp3v.com](https://myfreemp3v.com)_
Usage:
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
```
The script will save the song in the same directory as the `myFreeMp3` package, with the exact name of the song you searched for, with `.mp3` extension. 
