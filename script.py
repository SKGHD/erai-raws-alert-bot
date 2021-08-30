import feedparser
import time
from datetime import datetime
from pytz import timezone
import shortuuid
### Module imports ###
from config import connectAria2RPC
from handlers import *


############## Connecting to Aria2 RPC Server #########

aria2 = connectAria2RPC()


counter = 1
SERVER_START_TIME = datetime.now(timezone('Asia/Kolkata'))


while True:
    currentTime = datetime.now(timezone('Asia/Kolkata'))
    getList = feedparser.parse(
        "https://www.erai-raws.info/episodes/feed/?res=720p&type=magnet&subs%5B0%5D=us")
    namesList = []
    magnetList = []
    ########## Getting list of anime from DB############
    animeList = storeData(fetchData('animelist'))

    for i in range(len(getList.entries)):
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
