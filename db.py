from configparser import ConfigParser
from pymongo import MongoClient

parser = ConfigParser()

try:
    parser.read('config.ini')
    conn = MongoClient(parser.get('DATABASE', 'URL'))
    db = conn.hackathon
except Exception as e:
    ## TODO: Logging
    pass
