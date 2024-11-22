import jwt
from flask import request, jsonify

SECRET_KEY = 'rio_sangat_hebat'


def decode_jwt_token():
    token = request.json.get('token')
    if not token:
        return None

    try:
        decoded_data = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        return decoded_data
    except jwt.ExpiredSignatureError:
        return jsonify({'message': 'Token expired'}), 401
    except jwt.InvalidTokenError:
        return jsonify({'message': 'Invalid token'}), 401