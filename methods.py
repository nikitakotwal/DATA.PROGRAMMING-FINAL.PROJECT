import requests
from bs4 import BeautifulSoup
import pandas as pd
from pymongo import MongoClient
import certifi
import urllib

mongouri = "mongodb+srv://nimish:"+urllib.parse.quote("Pass@123")+"@cluster0.7p9xsiz.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongouri, tlsCAFile=certifi.where())
db = client.get_database('topsongs')
records = db.music


def getSongList():
    req = requests.get("https://music.apple.com/browse/top-charts/songs")
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, 'html.parser')
        parsedData = soup.find_all(class_="songs-list-row__song-name")
        songs = [song.string for song in parsedData]
        return songs


def getArtistList():
    req = requests.get("https://music.apple.com/browse/top-charts/songs")
    if req.status_code == 200:
        soup = BeautifulSoup(req.content, 'html.parser')
        parsedData = soup.find_all(class_="songs-list-row__link")
        artists = [artist.string for artist in parsedData]
        return artists


def updateTop50():
    while True:
        records.delete_many({})
        songs = getSongList()
        artists = getArtistList()
        df = pd.DataFrame(list(zip(songs, artists)), columns=['Track', 'Artist'])
        df.index += 1
        records.insert_many(df.to_dict('records'))
        return df
        

def trendingArtists():
    df = updateTop50()
    dfDict = df['Artist'].value_counts().head(5).to_dict()
    googleList = [["Artist", "No. of appearances in top 50"]]
    for k, v in dfDict.items():
        googleList.append([k, v])
    return googleList