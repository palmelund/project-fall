from connect_str import connect_str
from respond import respond
from model.user import *
from database.database_manager import *
import psycopg2


def lambda_handler(event, context):
    allCitizens = get_all_citizens()

    return build_response(str(200), allCitizens)
