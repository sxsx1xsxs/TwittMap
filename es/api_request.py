# Reference: https://pythonprogramming.net/twitter-api-streaming-tweets-python-tutorial/
# Reference: http://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-indexing.html
import json
from tweepy import Stream
from tweepy import OAuthHandler
from tweepy.streaming import StreamListener
from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from configobj import ConfigObj

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

MAX_TWITTS = 300000

class Listener(StreamListener): # Inheritance
    id = 1
    bulk_file = ''

    awsauth = AWS4Auth(AWS_ACCESS_KEY, AWS_SECRET_KEY, region, service)

    host = 'search-twittmap-25h4sga4tud7fjcedw32mwjsua.us-east-1.es.amazonaws.com'

    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )

    def on_data(self, data):
        self.bulk_file += '{ "index" : { "_index" : "twitts_10keys", "_type" : "twitter", "_id" : "' + str(self.id % MAX_TWITTS) + '" } }\n'

        self.bulk_file += json.dumps(json.loads(data)) + '\n'
        self.id += 1
        if self.id % 100 == 0:
            self.es.bulk(self.bulk_file)
            self.bulk_file = ''
            print("We have uploaded " + str(self.id) + " twitts")
        return True

    def on_error(self, status_code):
        print(status_code)

if __name__ == '__main__':
    auth = OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
    auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)

    twitterStream = Stream(auth, Listener())
    twitterStream.filter(track=['trump', 'columbia', 'china', 'sundaymorning', 'rockets', 'nyc', 'nba', 'google', 'facebook', 'job'], async=True)
