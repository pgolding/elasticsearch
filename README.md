# Elasticsearch: The Definitive Guide (Python) #

To help those who want to follow [the book](https://www.elastic.co/guide/en/elasticsearch/guide/master/index.html) using Python code, I reproduced the various example API calls using the two Python libraries:

*[Elasticsearch](http://elasticsearch-py.readthedocs.io/en/master/index.html)
*[Elasticsearch DSL](http://elasticsearch-dsl.readthedocs.io/en/latest/index.html)

My goal is to assist the reader/learner in understanding the mechanics of Elasticsearch whilst understanding the Python libs.

I recommend following the book whilst exercising the examples in the Kibana console (or CURL) and Python.

The Python examples are embedded in an iPython notebook so that it's easier to interact and document the flow.

The examples here mostly follow the exact same flow as the book, beginning with chapter "Seaching - The Basic Tools"

This is a WIP and I will continue to update it with all examples and then build out more complex examples as accompanying notebooks.

Note that the examples here assume the same setup as the examples in the book, namely a virgin instance of Elasticsearch (most likely on localhost) pre-populated with the [test data](https://github.com/pgolding/elasticsearch/blob/master/examples.json).

To populate the index, you can run the additional script first: [add docs to index](https://github.com/pgolding/elasticsearch/blob/master/populate.ipynb)
