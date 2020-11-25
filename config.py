import aria2p
from os import environ as env
from pymongo import MongoClient
from dotenv import load_dotenv

if env.get("APP_ENV") == "testing":
    load_dotenv()


############## aria2 configuration ################
def connectAria2RPC():
    aria2 = aria2p.API(
        aria2p.Client(
            host=env.get("ARIA_HOST"),
            port=env.get("ARIA_PORT"),
            secret=env.get("ARIA_SECRET")
        )
    )
    return aria2


############### Telegram Configuration #############

bot_token = env.get("TELEGRAM_BOT_TOKEN")
bot_chatID = env.get("TELEGRAM_CHAT_ID")


### Creating Connection to Database server ###
def createConnectionToDB():
    cluster = MongoClient(env.get("MONGO_DRIVER_KEY"))
    db = cluster["horriblesubsbot"]
    return cluster, db
