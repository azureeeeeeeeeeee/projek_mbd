from flask_restful import Resource
from db import mysql
from flask import jsonify, request, make_response
import bcrypt
import jwt
import datetime


SECRET_KEY = "rio_sangat_hebat"


class Login(Resource):
         
    def post(self):
         
        data = request.json

        try:

            cursor = mysql.connection.cursor()

            # Fetching specific user
            cursor.execute("CALL get_user(%s)", (data['name'],))
            user = cursor.fetchone()
            cursor.close()
            
            # Verify User
            if user:
                if bcrypt.checkpw(data['password'].encode('utf-8'), user[2].encode('utf-8')):
                    expiration_time = datetime.datetime.now() + datetime.timedelta(minutes=15)
                    exp_timestamp = int(expiration_time.timestamp())

                    token = jwt.encode({'id': user[0], 'role': user[3], 'exp': exp_timestamp}, SECRET_KEY, algorithm='HS256')
                    response = make_response(jsonify({'message': 'Login successful'}))
                    response.set_cookie(
                        'TOKEN',
                        token,
                        httponly=True,
                        secure=False,
                        samesite='Lax',
                        max_age=24*60*60
                    )
                    return response
                return make_response(jsonify({'message': 'Username or Password is incorrect'}), 404)
                
            return make_response(jsonify({'message': 'Username or Password is incorrect'}), 404)
        except Exception as e:
            return make_response(jsonify({'message': 'error occured', 'error': str(e)}), 500)