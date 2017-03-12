# Elasticsearch: The Definitive Guide (with Python examples) #

#### Versions: ####

##### Services:
* Kibana (5.2.2)
* Elasticsearch (5.2.2)

##### Python libs:
* elasticsearch (5.2.0)
* elasticsearch-dsl (5.1.0)

### What is this?

This is a set of Jupyter notebooks to help those who want to follow the book [Elasticsearch: The Definitive Guide](https://www.elastic.co/guide/en/elasticsearch/guide/master/index.html) using Python code in addition to the JSON API calls in the book. I have reproduced most of the example API calls, often in various ways, using the two Python libraries:

* [Elasticsearch](http://elasticsearch-py.readthedocs.io/en/master/index.html)
* [Elasticsearch DSL](http://elasticsearch-dsl.readthedocs.io/en/latest/index.html)

My goal is to assist the reader/learner in understanding the mechanics of Elasticsearch whilst understanding the Python libs.

I follow the structure of the book fairly closely (beginning with "Seaching - The Basic Tools") using identical chapter names and headings. I suggest to follow the book whilst exercising some examples in the Kibana console (or via CURL) and some in Python.

In true notebook fashion, the notebooks provide an interactive documented flow and a place to play. Where useful, I insert text from the guide so as to not break the flow too much (between the book and the notebooks).

Note that the examples here assume the same setup as the examples in the book, namely a virgin instance of Elasticsearch (most likely on localhost) pre-populated with the [test data](https://github.com/pgolding/elasticsearch/blob/master/examples.json).

The helper script (index.py) is available to populate/delete/reset the index at various times throughout the chapters. You don't need to touch it as I included initialization at the start of each chapter:

```python
import index

r = index.populate()
print('{} items created'.format(len(r['items'])))
```

If at any time you get stuck with the index, then just call ```index.populate()``` to delete and re-populate the index. You can also pass in a JSON object to define the settings and field mappings etc:

```python
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
index.populate(index_template)
```

(However, I usually make these calls where needed in the notebooks.)

This is a WIP and I will continue to update it with all examples and later build out more complex examples as accompanying notebooks.

Note that this is **not** a comprehensive coverage of all examples in the book. I have skipped a few examples here and there, mostly because they are repetitive or because they deal with non-English languages.

Also, I have added extra examples and included supplementary test data where useful (e.g. synonyms, stopwords files etc.) . This was to add further clarity of emphasis to some of the examples or to provide settings or info overlooked by the book (but covered in the API docs).