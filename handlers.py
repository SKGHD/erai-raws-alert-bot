from config import createConnectionToDB, bot_chatID, bot_token
import requests


############# MongoDB Configuration #############
cluster, db = createConnectionToDB()


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
