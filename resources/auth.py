from flask_restful import Resource
from db import mysql
from flask import jsonify, request, make_response
import bcrypt
import jwt


SECRET_KEY = "rio_sangat_hebat"


class Login(Resource):    
    def post(self):
        data = request.json

        cursor = mysql.connection.cursor()

        # Fetching specific user
        cursor.execute("CALL get_user(%s)", (data['name'],))
        user = cursor.fetchone()
        cursor.close()
        
        # Verify User
        if user:
            print(user)
            if bcrypt.checkpw(data['password'].encode('utf-8'), user[2].encode('utf-8')):
                token = jwt.encode({'id': user[0], 'role': user[3]}, SECRET_KEY, algorithm='HS256')
                response = make_response(jsonify({'message': 'Login successful'}))
                response.set_cookie(
                    'TOKEN',
                    token,
                    httponly=True,
                    secure=True,
                    samesite='Lax',
                    max_age=24*60*60
                )
                return response
            return jsonify({'message': 'Wrong password'})
            
        return jsonify({'message': 'User not found'})
