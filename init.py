from flask import Flask, render_template, request
from handlers import fetchData, storeData
from datetime import datetime
from pytz import timezone

app = Flask(__name__)


animeListContent = fetchData('animelist')


def loadAnimeList():
    global animeList
    animeList = storeData(animeListContent)


loadAnimeList()


@app.route('/')
def index():

    addNew = request.args.get('nameInput')
    if addNew != None:
        animeListContent.insert_one(
            {"name": addNew, "timestamp": datetime.now(timezone('Asia/Kolkata'))})
        loadAnimeList()

    return render_template('index.html', mylist=animeList, anime=addNew)


if __name__ == "__main__":
    app.run(debug=True)
