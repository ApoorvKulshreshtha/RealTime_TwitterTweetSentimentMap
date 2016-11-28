from watson_developer_cloud import AlchemyLanguageV1
import json
import boto3
import boto
from boto import sns
from concurrent.futures import ThreadPoolExecutor
import time
from kafka import KafkaConsumer

REGION = 'us-east-1'
TOPIC  = ''

conn = boto.sns.connect_to_region(REGION)

alchemy_language = AlchemyLanguageV1(api_key='')

consumer = KafkaConsumer(bootstrap_servers = 'localhost:9092',value_deserializer=lambda m: json.loads(m.decode('utf-8')))
consumer.subscribe(['Twitter_US'])

def process_tweets():
    for msg in consumer:
        try:
            js = json.loads(msg.value.decode('utf-8'))
            sns_doc={}
            coords = js[u'coordinates'][u'StringValue']
            tweet_text = js[u'text'][u'StringValue']
            senti_output = alchemy_language.sentiment(text = tweet_text)
            if senti_output['status'] == 'OK':
                senti_answer = senti_output['docSentiment']["type"]
                sns_doc['coordinates']= coords
                sns_doc['sentiment'] = senti_answer
                sns_doc['text']= tweet_text
				sns_doc['id']=js[u'id'][u'StringValue']
                snsInput = json.dumps(sns_doc)
                print snsInput
                pub = conn.publish(topic=TOPIC, message=snsInput)
                time.sleep(5)
                print pub
            else:
                print('Error in sentiment analysis calcultion ', senti_output['statusInfo'])
        except Exception, e:
            time.sleep(1)
            print e
            pass


def main():
    executor = ThreadPoolExecutor(max_workers=1)
    while True:
        executor.submit(process_tweets)

if __name__ == '__main__':
    main()
