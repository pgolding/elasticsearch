from elasticsearch import Elasticsearch
from pprint import pprint
import time
import uuid
from IPython.display import display_javascript, display_html, display
import json

es = Elasticsearch(
    'localhost',
    # sniff before doing anything
    sniff_on_start=True,
    # refresh nodes after a node fails to respond
    sniff_on_connection_fail=True,
    # and also every 60 seconds
    sniffer_timeout=60
)

# Shards = 1 because of https://www.elastic.co/guide/en/elasticsearch/guide/master/relevance-is-broken.html
index_template = {
  "settings": { "number_of_shards": 1 },
  "mappings": {
    "tweet" : {
      "properties" : {
        "tweet" : {
          "type" :    "text",
          "analyzer": "english"
        },
        "date" : {
          "type" :   "date"
        },
        "name" : {
          "type" :   "text"
        },
        "user_id" : {
          "type" :   "long"
        }
      }
    }
  }
}

# Shards = 1 because of https://www.elastic.co/guide/en/elasticsearch/guide/master/relevance-is-broken.html
multi_field_index_template = {
  "settings": { "number_of_shards": 1 },
  "mappings": {
    "tweet" : {
      "properties" : {
                
        "tweet": { 
            "type":     "string",
            "analyzer": "english",
            "fields": {
                "raw": { 
                    "type":  "string",
                    "index": "not_analyzed"
                        }
                      }
        },    
        "date" : {
          "type" :   "date"
        },
        "name" : {
          "type" :   "text"
        },
        "user_id" : {
          "type" :   "long"
        }
      }
    }
  }
}

f = open('../examples_main.json', 'r')
data = f.read()

def load_sid_examples(settings=None, set=None):
    if set==1:
        file_to_load='../examples_sid.json'
        idx = 'my_store'
        dt = 'produces'
    elif set==2:
        file_to_load='../examples_posts.json'
        idx = 'my_index'
        dt = 'posts'
    elif set==3:
        file_to_load='../examples_fox.json'
        idx = 'my_index'
        dt = 'my_type'        
    else:
        file_to_load='../examples_sid.json'
        idx = 'my_store'
        dt = 'produces'
        
    try:
        f = open(file_to_load, 'r')
        sid_data = f.read()
        if es.indices.exists(idx):
            es.indices.delete(idx)
        if settings:
            es.indices.create(index=idx, body=settings)  
        response = es.bulk(index=idx, doc_type=dt, body=sid_data)
    except Exception as e:
        print('Error loading examples')
        response = e
    return response

def reset_all():
    reset()
    if es.indices.exists('shows'):
        es.indices.delete(index='shows')
    if es.indices.exists('email'):
        es.indices.delete(index='email')
        
def create_my_index(index_name='my_index', body=None):
    if es.indices.exists(index_name):
        es.indices.delete(index_name)
    es.indices.create(index=index_name, body=body)
        
        
def populate(template_num=None):
    if es.indices.exists('gb'):
        es.indices.delete(index='gb')
        # cautious wait on index deletion - prob. not needed
        time.sleep(1)
    if es.indices.exists('us'):
        es.indices.delete(index='us')
        # cautious wait on index deletion - prob. not needed
        time.sleep(1)
    if isinstance(template_num, int):
        if template==1:
            es.indices.create(index='gb', body=index_template)
            response = es.bulk(body=data)
        elif template==2:
            es.indices.create(index='gb', body=multi_field_index_template)
            es.indices.create(index='us', body=multi_field_index_template)
            response = es.bulk(body=data)
    else:
        response = es.bulk(body=data)
    return response    
    

def populate_tweets_using_mapping(template=None):
    if es.indices.exists('gb'):
        es.indices.delete(index='gb')
        # cautious wait on index deletion - prob. not needed
        time.sleep(1)
    if es.indices.exists('us'):
        es.indices.delete(index='us')
        # cautious wait on index deletion - prob. not needed
        time.sleep(1)
    if isinstance(template, dict):
        es.indices.create(index='gb', body=template)
        es.indices.create(index='us', body=template)
        response = es.bulk(body=data)
    else:
        response = es.bulk(body=data)
    return response


def reset():
    if es.indices.exists('gb'):
        es.indices.delete(index='gb')
        time.sleep(1)
    if es.indices.exists('us'):
        es.indices.delete(index='us')
        time.sleep(1)
        
# A helped class to render long JSON objects from ES with collapsible elements
class RenderJSON(object):
    def __init__(self, json_data):
        if isinstance(json_data, dict):
            self.json_str = json.dumps(json_data)
        else:
            self.json_str = json_data
        self.uuid = str(uuid.uuid4())

    def _ipython_display_(self):
        display_html('<div id="{}" style="height: 600px; width:100%;"></div>'.format(self.uuid), raw=True)
        display_javascript("""
        require(["https://rawgit.com/caldwell/renderjson/master/renderjson.js"], function() {
        document.getElementById('%s').appendChild(renderjson(%s))
        });
        """ % (self.uuid, self.json_str), raw=True)

reset_all()