from flask import Flask, render_template, redirect, request, jsonify
from flask import make_response
from elasticsearch import Elasticsearch
import json, time, threading


application = Flask(__name__)
keywordGlobal = ""
sh_index = 'tweetfinal'
@application.route("/")
def home():
    #fetch the es instance
    es = getESInstance()

    #call es search without any keywords
    result = es.search(size=5000,index=sh_index)

    #return parsed result with rerender
    return render_template('final_template.html', result=parseRes(result))

@application.route('/keysearch', methods = ['GET','POST'])
def keysearch():
    #extracting the keywords from the search query
    keywords = request.form['search']
    
    #call es using keywords
    es = getESInstance()

    #update global keyword list
    updateKeywords(str(keywords))

    #call happens inside getMatchedTweets
    result = getMatchedTweets(es, str(keywords))

    #return parsed result with rerender
    return render_template('final_template.html', result=parseRes(result))

def getESInstance():
  #create and return new es instance based on host
  es = Elasticsearch([{'host':'search-twitttrends-maoovmmsk27kusouc5bwzn2nuq.us-east-1.es.amazonaws.com', 'port':443,'use_ssl':True}])
  return es

def getMatchedTweets(es, keyword):
    #extra check here for an empty keyword string inputed from form
    if len(keyword) is not 0:
      res = es.search(size=5000, index=sh_index, body={"query": {"query_string": {"query": keyword}}})
    else:
      res = es.search(size=5000,index=sh_index)

    #return result of es search with keywords  
    return res

def updateKeywords(keywordList):
  #update global keyword list
  global keywordGlobal
  keywordGlobal = keywordList

def parseRes(result):
  #parsing results
  for r in result['hits']['hits']:
    #in each record, remove non-unicode chars from the tweet text (emoticons etc)
    r['_source']['text'] = ''.join(i for i in r['_source']['text'] if ord(i)<128)
  return result

@application.route('/rt', methods = ['GET','POST'])
def rt():
    #the real time tweet logic
    #fetching the es instance
    es = getESInstance()

    #retrieving global keywords
    global keywordGlobal

    #fetching based on keywords
    if len(keywordGlobal) is not 0:
        result = es.search(size=5000, index=sh_index, body={"query": {"query_string": {"query": keywordGlobal}}})
    else:
        result = es.search(size=5000,index=sh_index)
  
    #returning returnecd result without rerender
    return jsonify(parseRes(result))



def parse_tweets(msg):
    msg_doc= {}
    msg2 = json.loads(msg)
    print "FINAL RUN"
    print "MSG2 IS"
    print type(msg2)
    print "MSG2 COORD IS"
    print type(msg2['coordinates'])
    msg3 = json.loads(msg2['coordinates'])
    print "MSG2 COORD COORD IS"
    print type(msg3['coordinates'])
    print "1st ELEMENT"
    print msg3['coordinates'][0]
    msg_doc['positionx'] = msg3['coordinates'][1]
    msg_doc['positiony'] = msg3['coordinates'][0]
    # msg_doc[coordinates] = [msg3['coordinates'][1], msg3['coordinates'][0]]
    msg_doc['sentiment'] = msg2['sentiment']
    msg_doc['text'] = msg2['text']
    return msg_doc



def msg_process(msg, tstamp):
    print "trying to find the error"
    print msg
    msg=parse_tweets(msg)
    es = Elasticsearch([{'host': 'search-tweets-cxx6vzzzsobvc3ipbzrk3dreky.us-west-2.es.amazonaws.com', 'port': 443, 'use_ssl': True}])
    print "DONE1"
    es.index(index='senti_twitter', doc_type='senti_tweets', ttl="4d", body=msg)
    print "DONE2"

@application.route('/trying', methods=['GET', 'POST', 'PUT'])
def sns():
    # AWS sends JSON with text/plain mimetype
    try:
        js = json.loads(request.data)


    except Exception, e:
        print "Exception here"

    print "I am here"
    hdr = request.headers.get('X-Amz-Sns-Message-Type')
    # subscribe to the SNS topic
    if hdr == 'SubscriptionConfirmation' and 'SubscribeURL' in js:
        r = requests.get(js['SubscribeURL'])

    if hdr == 'Notification':
        msg_process(js['Message'], js['Timestamp'])

    return 'OK\n'





@application.route('/geospatial', methods = ['GET','POST'])
def geospatial():
    #fetch latitude and longitude
    latitude = request.args.get('lat', 0, type=float)
    longitude = request.args.get('long', 0, type=float)
  
    es = getESInstance()
    global keywordGlobal
    return jsonify(1);




if __name__ == "__main__":
  try:
	  application.run(port=8000)
  except Exception,e:
      print (e)
      print('socket failure. Gracful exit. Please try again. Should work')
