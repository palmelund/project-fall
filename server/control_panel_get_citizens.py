from connect_str import connect_str
from respond import respond
from model.user import *
import psycopg2


def lambda_handler(event, context):
    allCitizens = []
