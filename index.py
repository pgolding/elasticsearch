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

index_template = {
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

multi_field_index_template = {
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

f = open('../examples.json', 'r')
data = f.read()

def reset_all():
    reset()
    if es.indices.exists('shows'):
        es.indices.delete(index='shows')
    if es.indices.exists('email'):
        es.indices.delete(index='email')

def populate(template=None):
    response = None
    if es.indices.exists('gb'):
        es.indices.delete(index='gb')
        time.sleep(2)
    if es.indices.exists('us'):
        es.indices.delete(index='us')
        time.sleep(2)
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


def reset():
    if es.indices.exists('gb'):
        es.indices.delete(index='gb')
        time.sleep(1)
    if es.indices.exists('us'):
        es.indices.delete(index='us')
        time.sleep(1)
        

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