from flask import Flask, request
from flask_cors import CORS
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from configobj import ConfigObj
import json
import random
from es_conn import es_conn
PATH_TO_INI = './keys.ini'

application = Flask(__name__)
CORS(application)

@application.route('/')
def hello_world():
    return 'Hello World!'

@application.route('/keyword/<keyword>/size/<int:size>')
def show_twitts(keyword, size):
    es = es_conn(PATH_TO_INI)
    dict = es.search(index="twitters", doc_type="twitter", q = keyword, size = size)['hits']['hits']
    search_result = []
    for row in dict:
         id = row['_source']['id']
         text = row['_source']['text']
         if not row['_source']['geo']:
             coordinates = [random.triangular(-90, 90), random.triangular(-180, 180)] 
         else:
             coordinates = row['_source']['geo']['coordinates']
         search_result.append({'id' : id, 'text' : text, 'coordinates': coordinates})
    return json.dumps(search_result)

@application.route('/distance/<distance>/lat/<float:lat>/lon/<float:lon>')
def geo_search(distance, lat, lon):
    es = es_conn(PATH_TO_INI)
    obj = {"query": {"bool": {"must": {"match_all" : {}}, "filter": {"geo_distance": {"distance": distance+"km", "cor2" : {"lat": lat - 90, "lon" : lon - 180}}}}}}
    dict = es.search(index="twitters", doc_type="twitter", body = json.dumps(obj), size = 4000)['hits']['hits']
    search_result = [] 
    for row in dict:
         if 'id' not in row['_source'] or 'text' not in row['_source']:
             continue
         id = row['_source']['id']
         text = row['_source']['text']
         if not row['_source']['geo']:
             coordinates = [random.triangular(-90, 90), random.triangular(-180, 180)]
         else:
             coordinates = row['_source']['geo']['coordinates']
         search_result.append({'id' : id, 'text' : text, 'coordinates': coordinates})
    return json.dumps(search_result)
