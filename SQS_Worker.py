from watson_developer_cloud import AlchemyLanguageV1
import json
import boto3
import boto
from boto import sns
from concurrent.futures import ThreadPoolExecutor
import time

REGION = 'us-west-2'
TOPIC  = ''
conn = boto.sns.connect_to_region( REGION )

queueName = "tweets"
alchemy_language = AlchemyLanguageV1(api_key='')


sqs = boto3.resource('sqs')
queue = sqs.get_queue_by_name(QueueName=queueName)


def process_tweets():
	for message in queue.receive_messages(MessageAttributeNames=['All']):
		if message.message_attributes is not None:
			sns_doc={}
			coords = message.message_attributes.get('coordinates').get('StringValue')
			senti_output = alchemy_language.sentiment(text = message.body)
			if senti_output['status'] == 'OK':
				senti_answer =  senti_output['docSentiment']
				sns_doc['coordinates']= coords
				sns_doc['sentiment'] = senti_answer
				sns_doc['text']= message.body
				sns_doc['id'] = message.message_attributes.get('id').get('StringValue')
				print sns_doc
				snsInput = json.dumps(sns_doc)
				pub = conn.publish(topic=TOPIC, message=snsInput)
				time.sleep(4)
			else:
				print('Error in sentiment analysis calcultion ', senti_output['statusInfo'])
			message.delete()	

def main():
    executor = ThreadPoolExecutor(max_workers=10)
    while True:
        executor.submit(process_tweets)

if __name__ == '__main__':
    main()				