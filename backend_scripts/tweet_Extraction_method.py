import tweepy
from elasticsearch import Elasticsearch

access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

#Using Tweepy REST APIs

MyTweepyObject = tweepy.API(auth)

CountryCodes = MyTweepyObject.geo_search(query="India", granularity="country")
Country_ID = CountryCodes[0].id

Elastic_Search_Object = Elasticsearch(
    [{'host': 'search-tweetmap-4qeqqxxkmf62ajq6djhqwvlzni.us-east-1.es.amazonaws.com', 'port': 443, 'use_ssl': True}])

counterLim = 100
tweetIter = 0
#Elastic_Search_Object.create('twitter')

mapping = {

    'coordinates': {

        'type': 'geo_point'
    }

}
#Elastic_Search_Object.indices.create(index='twitters', ignore=400, body=mapping)

while tweetIter < counterLim:

    TweetList = MyTweepyObject.search(q="place:%s" % Country_ID, count=50)
    for CurrentTweet in TweetList:

        if not CurrentTweet.coordinates:
            continue

        Elastic_Tweet = {}
        if CurrentTweet.place:
            Elastic_Tweet['place'] = CurrentTweet.place.full_name
        Elastic_Tweet['user-name'] = CurrentTweet.user.name
        Elastic_Tweet['id'] = CurrentTweet.id
        Elastic_Tweet['text'] = CurrentTweet.text
        Elastic_Tweet['user-id'] = CurrentTweet.user.id
        Elastic_Tweet['hashtag'] = [hashtag['text'] for hashtag in CurrentTweet.entities['hashtags']]
        Elastic_Tweet['coordinates'] = CurrentTweet.coordinates['coordinates']
        Elastic_Search_Object.index(index='twitters', doc_type='tweets', id=CurrentTweet.id, body=Elastic_Tweet)
        print ('inserted')

    tweetIter += len(TweetList)

