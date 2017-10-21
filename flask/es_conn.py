from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
from configobj import ConfigObj

def es_conn(path_to_ini):
    config = ConfigObj(path_to_ini)
    es_config = config['es']
    ACCESS_KEY = es_config['ACCESS_KEY']
    SECRET_KEY = es_config['SECRET_KEY']
    region = es_config['region']
    service = es_config['service']
    host = es_config['host']
    awsauth = AWS4Auth(ACCESS_KEY, SECRET_KEY, region, service)
    es = Elasticsearch(
        hosts=[{'host': host, 'port': 443}],
        http_auth=awsauth,
        use_ssl=True,
        verify_certs=True,
        connection_class=RequestsHttpConnection
    )
    return es
