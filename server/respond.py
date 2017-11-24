import json


def respond(err, res=None):
    return {
        'statusCode': '400' if err else '200',
        'body': err.message if err else json.dumps(res),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def build_response(statuscode, message):
    return {
        'statusCode': '\'' + statuscode + '\'',
        'body': json.dumps(message),
        'headers': {
            'Content-Type': 'application/json',
        },
    }


def build_response_no_ser(statuscode, message):
    return {
        'statusCode': '\'' + statuscode + '\'',
        'body': message,
        'headers': {
            'Content-Type': 'application/json',
        },
    }

