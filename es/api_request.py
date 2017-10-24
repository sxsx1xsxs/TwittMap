# Reference: https://pythonprogramming.net/twitter-api-streaming-tweets-python-tutorial/
# Reference: http://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-indexing.html
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from configobj import ConfigObj
import random
import time

PATH_TO_INI = '..\\config\\keys.ini'
config = ConfigObj(PATH_TO_INI)
twitter_config = config['Twitter']
es_config = config['es']

CONSUMER_KEY = twitter_config['CONSUMER_KEY']
CONSUMER_SECRET = twitter_config['CONSUMER_SECRET']
ACCESS_KEY = twitter_config['ACCESS_KEY']
ACCESS_SECRET = twitter_config['ACCESS_SECRET']
AWS_ACCESS_KEY = es_config['ACCESS_KEY']
AWS_SECRET_KEY = es_config['SECRET_KEY']
region = es_config['region']
service = es_config['service']
host = es_config['host']

MAX_TWITTS = 50000

lat1 = (45, 69)
long1 = (17, 135)
lat2 = (8, 30)
long2 = (-7, 37)
lat3 = (38, 65)
long3 = (-121, 81)
lat4 = (-36, -20)
long4 = (120, 147)
area = [(lat1, long1), (lat1, long1), (lat2, long2), (lat3, long3), (lat3, long3), (lat4, long4)]

class Listener(StreamListener): # Inheritance
    id = 1
    bulk_file = ''

    awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, region, service)

    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    def on_data(self, data):
        self.bulk_file += '{ "index" : { "_index" : "twitters", "_type" : "twitter", "_id" : "' + str(self.id % MAX_TWITTS) + '" } }\n'
        dict = json.loads(data)

        if 'geo' in dict and dict['geo'] is not None:
            cor = dict['geo']['coordinates']
            dict['cor2'] = {"lat": cor[0], "lon": cor[1]}
        elif 'geo' not in dict or dict['geo'] is None:
            index = random.randint(0, len(area) - 1)
            lat = random.uniform(area[index][0][0], area[index][0][1])
            long = random.uniform(area[index][1][0], area[index][1][1])
            dict['geo'] = {'type' : 'Point', 'coordinates' : [lat, long]}
            dict['cor2'] = {"lat": lat, "lon": long}
        # print(dict)
        self.bulk_file += json.dumps(dict) + '\n'
        self.id += 1
        if self.id % 100 == 0:
            self.es.bulk(self.bulk_file)
            self.bulk_file = ''
            time.sleep(0.1)
            print("We have uploaded " + str(self.id) + " twitts")
        if self.id >=MAX_TWITTS:
            self.id = 1
        return True

    def on_error(self, status_code):
        print(status_code)

if __name__ == '__main__':
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    twitterStream = Stream(auth, Listener())
    twitterStream.filter(track=['trump', 'columbia', 'china', 'sundaymorning', 'rockets', 'nyc', 'nba', 'google', 'facebook', 'job'], stall_warnings=True, async=True)

