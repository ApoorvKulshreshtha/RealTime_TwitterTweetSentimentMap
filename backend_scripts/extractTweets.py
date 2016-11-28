import json
import time
from elasticsearch import Elasticsearch

#import twitter keys and tokens
from config import *

# create instance of elasticsearch
es = Elasticsearch( [{'host':'', 'port':443,'use_ssl':True}])
print es.info()

access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from textblob import TextBlob

count = 1
count2 = 1
class TweetStreamListener(StreamListener):

    # on success
    def on_data(self, data):
        if(data == None):
            return
        #decode json
        try:
            dict_data = json.loads(data)
        except:
            return
        global count
        count = count + 1
        print (count)
        try:

            #print (dict_data['coordinates'])
            cache_index = {}

            cache_index['id'] = dict_data['id']
            cache_index['text'] = dict_data['text']
            cache_index['user-name'] = dict_data['user']['name']
            cache_index['user-id'] = dict_data['user']['id']
            cache_index['hashtag'] = [ht['text'] for ht in dict_data['entities']['hashtags']]
            cache_index['coordinates'] = dict_data['coordinates']
            cache_index['retweet-count'] = dict_data['retweet_count']
            cache_index['favorite-count'] = dict_data['favorite_count']
            es.create(index='wands', params=dict(), id=cache_index['id'], doc_type='json/data', body=cache_index)
            if(dict_data['coordinates']):
                #print 'inserted'
                #print (dict_data['coordinates'])
                global count2
                count2 = count2 + 1
                print 'GEO ',count2
        except:
            return
        #print ("inserted", count)
        time.sleep(0.1)
        return True

    # on failure
    def on_error(self, status):
        time.sleep(0.1)
        if(status == 420):
            time.sleep(10)
        #print status

def getTweets():

    # create instance of the tweepy tweet stream listener
    listener = TweetStreamListener()

    # set twitter keys/tokens
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # create instance of the tweepy stream
    stream = Stream(auth, listener)

    # search twitter for "congress" keyword
    GEOBOX_WORLD = [-180, -90, 180, 90]
    for i in range(1,11):
        try:
            #stream.filter(track=["trump"])
            stream.filter(locations=GEOBOX_WORLD)
            #stream.sample()
        except:
           time.sleep(10)
           continue
getTweets()