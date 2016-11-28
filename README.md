#Real Time Twitter Tweet Sentiment Map


This project was done as part of Cloud Computing and Big Data course at Columbia University (Fall 2016).


Project Collaborators: Apoorv Kulshreshtha ak3963, Yogeshwar Mutneja ym2578


Requirements

1. AWS SQS

2. AWS SNS

3. AWS ElasticBeanStalk

4. Apache Kafka

5. Elastic Search

6. IBM AlchemyAPI

7. Flask


 
Project modules:

1. Stream tweets from Twitter and store them into AWS SQS or Apache Kafka

2. Fetch tweets from SQS/Kafka and do sentiment analysis on it using AlchemyAPI

3. Once the tweet has been processed, publish it to SNS

4. SNS sends notification to Flask backend, which then stores the tweet in ElasticSearch and also displays the tweet on the frontend map.


Below is the architecture diagram of the project:

![alt tag](http://i.imgur.com/ouIDUJT.png)


Following is the link to the project deployed on EBS:
http://flask4.yj7reggdi8.us-west-2.elasticbeanstalk.com/
