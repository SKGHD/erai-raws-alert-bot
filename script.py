import feedparser
import requests
import time
import aria2p
from pymongo import MongoClient
from datetime import datetime
from pytz import timezone
from os import environ as env


############## aria2 configuration ################
aria2 = aria2p.API(
    aria2p.Client(
        host=env.get("ARIA_HOST"),
        port=env.get("ARIA_PORT"),
        secret=env.get("ARIA_SECRET")
    )
)
############### Telegram Configuration #############
bot_token = env.get("TELEGRAM_BOT_TOKEN")
bot_chatID = env.get("TELEGRAM_CHAT_ID")

counter = 1
SERVER_START_TIME = datetime.now(timezone('Asia/Kolkata'))

# fetching data from mongo server


def fetchData(collectionName):
    cluster = MongoClient(env.get("MONGO_DRIVER_KEY"))
    db = cluster["horriblesubsbot"]
    collection = db[collectionName]
    return collection


def storeData(collection):
    documentList = []
    results = collection.find({})
    for result in results:
        documentList.append(result["name"])
    return documentList


while True:
    currentTime = datetime.now(timezone('Asia/Kolkata'))
    getList = feedparser.parse("https://www.erai-raws.info/rss-720-magnet")
    namesList = []
    magnetList = []
    ########## Getting list of anime from DB############
    animeList = storeData(fetchData('animelist'))

    for i in range(50):
        namesList.append(getList.entries[i].title)
        magnetList.append(getList.entries[i].link)

    def sendMsg(k):
        msg = f"New episode available = {namesList[k]} "
        send_text = 'https://api.telegram.org/bot' + bot_token + \
            '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=HTML&text=' + msg
        requests.get(send_text)
        # Adding to my Download tasks
        aria2.add_magnet(magnetList[k])

    def getLastID():
        lastID = fetchData("completedjobs").count_documents({})
        return(lastID + 1)

    def updateContent():
        # get all name: key values and store them in a list called completedJobs then return (completedJobs)
        completedJobs = storeData(fetchData("completedjobs"))
        return (completedJobs)

    def updateDB(newItem):
        # post new update to database
        updateTime = currentTime.strftime("%d-%m-%y %I:%M:%S %p")
        post = {"_id": getLastID(), "name": newItem, "date": updateTime}
        fetchData("completedjobs").insert_one(post)
        print(f'Added to the database "completedjobs" = {newItem}')

    for i in animeList:
        print(f'Searching for {i} in RSS feed')
        if str(i) in str(namesList):
            # index of namesList item which matched with animeList
            k = [idx for idx, s in enumerate(namesList) if i in s][0]
            completedJobscontent = updateContent()
            if (namesList[k] in str(completedJobscontent)) == False:
                print(f'Found new Episode: {namesList[k]}')
                updateDB(namesList[k])
                sendMsg(k)
    ###################Bunch of STDOUTS################################
    print(f'Server running since {SERVER_START_TIME}')
    print(f"Current Time : {datetime.now(timezone('Asia/Kolkata'))}")
    print(f'I have looped for {counter} times since server start')
    print(f'I will now sleep for 15 mins')
    counter += 1
    time.sleep(900)
