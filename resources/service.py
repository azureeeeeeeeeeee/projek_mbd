import jwt
from flask import request, jsonify, make_response
from datetime import datetime

SECRET_KEY = 'rio_sangat_hebat'


def decode_jwt_token():
    token = request.cookies.get('TOKEN')
    if not token:
        return None
    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        if datetime.now().timestamp() > decoded_data['exp']:
            raise Exception('Token expired')
        return decoded_data
    except jwt.InvalidTokenError:
        raise Exception('Token invalid')


def cursor_to_json(cursor, rows):
    cols = [col[0] for col in cursor.description]
    data = [dict(zip(cols, row)) for row in rows]

    return data



