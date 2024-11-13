from flask_restful import Resource
from db import mysql
from flask import jsonify, request
import bcrypt


class User(Resource):
    def post(self):
        # DATA : email, fullname, password, is_admin
        data = request.json

        # Hash password dari user
        password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        # Execute query
        cursor = mysql.connection.cursor()
        cursor.execute(
            "CALL create_user(%s, %s, %s, %s)", 
            (data['email'], data['fullname'], password, data['is_admin'])
        )

        mysql.connection.commit()
        cursor.close()
        return jsonify({"message": "User created"})