import requests
from pydub import AudioSegment
import base64

sound = AudioSegment.from_mp3("Sag My Pants Hopsin.mp3")

url = "https://shazam.p.rapidapi.com/songs/detect"

payload = sound.raw_data[:5000]


headers = {
    'x-rapidapi-host': "shazam.p.rapidapi.com",
    'x-rapidapi-key': "4cebbd04d9msh0d52cfd9b0766e3p1de687jsn6b3358a07e4f",
    'content-type': "text/plain",
    'accept': "text/plain"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
