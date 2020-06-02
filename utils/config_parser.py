# Creates a parser for the configurations/config.ini

# Importing all the required libraries.
from configparser import ConfigParser

parser = ConfigParser()
parser.read('configurations/config.ini')
