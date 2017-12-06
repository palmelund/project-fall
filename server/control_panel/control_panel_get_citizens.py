import DatabaseManager


def lambda_handler(event, context):
    DatabaseManager.get_all_citizens()
