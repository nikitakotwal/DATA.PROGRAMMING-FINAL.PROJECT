from flask import Flask, render_template
import methods
from bs4 import BeautifulSoup
import pandas as pd
import time
from pymongo import MongoClient
import certifi
import urllib

app = Flask(__name__)

mongouri = "mongodb+srv://nimish:"+urllib.parse.quote("Pass@123")+"@cluster0.7p9xsiz.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongouri, tlsCAFile=certifi.where())
db = client.get_database('topsongs')
records = db.music


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/index.html")
def index():
    return render_template("index.html")


@app.route("/top50")
def top50():
    songs = records.find({})
    return render_template('Top50.html', songs=songs)


@app.route("/trendingArtists")
def trending():
    data = methods.trendingArtists()
    print(data)
    return render_template("trendingArtists.html", data=data)

@app.route("/trendingArtists2")
def trending2():
    data = methods.trendingArtists()
    print(data)
    return render_template("trendingArtists2.html", data=data)

########### apis to test #############

# top 'n' trending artists
@app.route("/getTopArtists")
def getTrendingArtists():
    methods.records.delete_many({})
    artists = methods.getArtistList()
    artistsDict = {}
    for artist in set(artists):
        artistsDict[artist]=str(artists.count(artist)) + " Titles"
    return artistsDict

# top 200 titles and artists
@app.route("/getTop200")
def getTop200():
    methods.records.delete_many({})
    songs = methods.getSongList()
    artists = methods.getArtistList()
    return dict(zip(songs, artists))

#######################################

if __name__ == "__main__":
    app.run(debug=True)

    while True:

        # refresh records every 24 hrs
        records.delete_many({})
        songs = methods.getSongList()
        artists = methods.getArtistList()
        df = pd.DataFrame(list(zip(songs, artists)), columns=['Track', 'Artist'])
        df.index += 1
        records.insert_many(df.to_dict('records'))

        time.sleep(86400)