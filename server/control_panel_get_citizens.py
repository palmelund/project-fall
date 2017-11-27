from connect_str import connect_str
from respond import respond
from model.user import *
import psycopg2
import json
import DatabaseManager


def lambda_handler(event, context):
    DatabaseManager.get_all_citizens()