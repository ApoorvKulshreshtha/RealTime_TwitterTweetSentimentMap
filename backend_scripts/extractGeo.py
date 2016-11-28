import json
import time
from elasticsearch import Elasticsearch

#import twitter keys and tokens
from config import *

# create instance of elasticsearch
es = Elasticsearch( [{'host':'', 'port':443,'use_ssl':True}])
print es.info()

def getMatchedTweets(es, keyword):
    #res = es.search(index="2", doc_type='json/data', body={"query": {"query_string": {"query": keyword}}})
    res = es.search(size=5, index="wands", doc_type='json/data', body={"query": {"query_string": {"query": keyword}}})
    print res
    return res['hits']['hits']

def getMatchedGeoTweets(es, lati, longi):
    res = es.search(size=5000, index='wands', doc_type='json/data', body={ "query": {
        "query_string": {
            "query": "_exists_:coordinates"
        }
    }})
    res = es.search(size=5000, index='wands', doc_type='json/data', body={"query": {
    "bool" : {
        "must" : {
            "match_all" : {}
        },
        "filter" : {
            "geo_distance" : {
                "distance" : "100km",
                "coordinates" : [lati, longi]
            }
        }
    }
}})
#print (len(res['hits']['hits']))
#return res['hits']['hits']

#getMatchedTweets(es,'the')
#getMatchedGeoTweets(es)
