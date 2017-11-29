import requests
import json
import datetime
import time
from pymongo import MongoClient

default_retries = 5
default_wait = 30 # 30 seconds
succeeds = False
retries = 0

# Mongo client
client = MongoClient('mongodb', 27017)

def wait_and_retry():
    global retries
    retries += 1
    print("retrying in %d seconds..." % default_wait)
    time.sleep(default_wait)

while not succeeds and retries < default_retries:
    # Request top 10 criptocoin
    url = 'https://api.coinmarketcap.com/v1/ticker/?limit=10'
    print("Requesting...", datetime.datetime.now())
    try:
        r = requests.get(url)

        coins = json.loads(r.content)

        # Include time
        for coin in coins:
            coin["date"] = datetime.datetime.now()

        # Insert on mongo
        db = client['criptocoins']
        succeeds = db.coinmarketcap.insert_many(coins).acknowledged
        if not succeeds:
            wait_and_retry()
    except:
        print("fail on fetch (%s)" % datetime.datetime.now())
        wait_and_retry()
