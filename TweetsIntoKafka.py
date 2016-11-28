from kafka import KafkaProducer
import tweepy
import time
import json

producer = KafkaProducer(bootstrap_servers = 'localhost:9092',value_serializer=lambda v: json.dumps(v).encode('utf-8'))
consumer_key=""
consumer_secret=""
access_token=""
access_token_secret=""

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

# Authentication
api = tweepy.API(auth)
# Add location
places = api.geo_search(query="United States", granularity="country")
place_id = places[0].id

for k in range(10):
        data = api.search(q="place:%s" % place_id, count = 100)
        for singleTweet in data:
            try:
                if not singleTweet.coordinates:
                    continue
                if singleTweet.lang != "en":
                    continue
                tweet_text = singleTweet.text
                tweet_text_filtered = ''.join(i for i in tweet_text if ord(i)<128 and ord(i) > 65 or ord(i) == 32 )
                tweet_place = ''
                if singleTweet.place:
                    tweet_place = singleTweet.place.full_name
                tweet_created_at = ''
                if singleTweet.created_at:
                    tweet_created_at = singleTweet.created_at.strftime("%Y-%m-%d %H:%M:%S")
                msgAttr = {
					"id":{
						'StringValue':singleTweet.id,
						'DataType' : 'String'
					},
                    "user_name": {
                        'StringValue': singleTweet.user.name,
                        'DataType' : 'String'
                    },
                    "coordinates":{
                        'StringValue': json.dumps(singleTweet.coordinates),
                        'DataType': 'String'
                    },
                    "place":{
                        'StringValue':tweet_place,
                        'DataType':'String'
                    },
                    "created-at":{
                        'StringValue': tweet_created_at,
                        'DataType':'String'
                    },
                    "text":{
                        'StringValue': tweet_text_filtered,
                        'DataType':'String'
                    }
                }
                js = json.dumps(msgAttr)
                producer.send('Twitter_US',js)
                print "now saving tweet: ", js
                time.sleep(1)
            except Exception, e:
                time.sleep(1)
                print e
                pass
producer.flush()