from flask import Flask, render_template
from handlers import fetchData, storeData

app = Flask(__name__)


@app.route('/')
def index():
    animeList = storeData(fetchData('animelist'))
    return render_template('index.html', mylist=animeList)


if __name__ == "__main__":
    app.run()
