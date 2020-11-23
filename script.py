import feedparser
import requests
import time
import aria2p
from pymongo import MongoClient
from datetime import datetime
from pytz import timezone
from os import environ as env
import shortuuid


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

### Creating Connection to Database server ###
cluster = MongoClient(env.get("MONGO_DRIVER_KEY"))
db = cluster["horriblesubsbot"]


# fetching data from mongo server
def fetchData(collectionName):
    collection = db[collectionName]
    return collection


# storing fetched data to a list
def storeData(collection):
    documentList = []
    results = collection.find({})
    for result in results:
        documentList.append(result["name"])
    return documentList

# Sending msg to telegram bot


def sendMsg(episodeName):
    msg = f"New episode available = {episodeName} "
    send_text = 'https://api.telegram.org/bot' + bot_token + \
        '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=HTML&text=' + msg
    requests.get(send_text)


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

    completedJobsCollection = fetchData("completedjobs")

    def updateDB(newItem):
        # post new update to database
        updateTime = currentTime.strftime("%d-%m-%y %I:%M:%S %p")
        post = {"_id": shortuuid.uuid(), "name": newItem, "date": updateTime}
        completedJobsCollection.insert_one(post)
        print(f'Added to the collection "completedjobs" = {newItem}')

    for i in animeList:
        print(f'Searching for {i} in RSS feed')
        if str(i) in str(namesList):
            # index of namesList item which matched with animeList
            k = [idx for idx, s in enumerate(namesList) if i in s][0]

            # Updating completedJobsList with latest documents
            completedJobsList = storeData(completedJobsCollection)
            # If an episode is not already in the list then execute these tasks
            if (namesList[k] in str(completedJobsList)) == False:
                print(f'Found new Episode: {namesList[k]}')
                updateDB(namesList[k])
                sendMsg(namesList[k])
                # Adding to my Download tasks
                aria2.add_magnet(magnetList[k])

###################Bunch of STDOUTS################################

    print(f'Server running since {SERVER_START_TIME}')
    print(f"Current Time : {datetime.now(timezone('Asia/Kolkata'))}")
    print(f'I have looped for {counter} times since server start')
    print(f'I will now sleep for 15 mins')
    counter += 1
    time.sleep(900)
