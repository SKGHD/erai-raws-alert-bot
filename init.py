from flask import Flask, render_template
from script import fetchData, storeData
from handlers import createConnectionToDB


app = Flask(__name__)


@app.route('/')
def index():
    cluster, db = createConnectionToDB()
    animeList = storeData(fetchData('animelist'))
    return render_template('index.html', mylist=animeList)


if __name__ == "__main__":
    app.run(debug=True)
