# Creates a Db connection.

# Importing all required libraries.
from pymongo import MongoClient

# Importing all required modules.
from utils.config_parser import parser

try:
    conn = MongoClient(parser.get('DATABASE', 'URL'))
    db = conn.hackathon
except Exception as e:
    print(e)
