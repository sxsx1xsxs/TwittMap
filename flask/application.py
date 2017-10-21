from flask import Flask, request
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from configobj import ConfigObj
import json
import random
from es_conn import es_conn
PATH_TO_INI = './keys.ini'

application = Flask(__name__)

@application.route('/')
def hello_world():
    return 'Hello World!'

@application.route('/keyword/<keyword>/size/<int:size>')
def show_twitts(keyword, size):
    es = es_conn(PATH_TO_INI)
    dict = es.search(q = keyword, size = size)['hits']['hits']
    search_result = []
    for row in dict:
         id = row['_source']['id']
         text = row['_source']['text']
         if not row['_source']['geo']:
             coordinates = [random.triangular(-90, 90), random.triangular(-180, 180)] 
         else:
             coordinates = row['_source']['coordinates']['coordinates']
         search_result.append({'id' : id, 'text' : text, 'coordinates': coordinates})
    return json.dumps(search_result)
