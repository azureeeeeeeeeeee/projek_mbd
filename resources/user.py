from flask_restful import Resource
from db import mysql
from flask import jsonify, request, make_response
import bcrypt
from . import service


class User(Resource):
    def get(self):
        try:
            user = service.decode_jwt_token()

            if not user['role']:
                return make_response(jsonify({'message': 'kamu tidak memiliki akses'}), 403)

            cursor = mysql.connection.cursor()
            cursor.execute('CALL get_all_users()')
            rows = cursor.fetchall()
            data = service.cursor_to_json(cursor, rows)
            return jsonify({'message': 'user fetched', 'users': data})

        except Exception as e:
            return make_response(jsonify({'message': 'error occured', 'error': str(e)}), 500)

    def post(self, user_type):
        # DATA : email, fullname, password, is_admin
        data = request.json

        if user_type == 'user':
            try:
                user = service.decode_jwt_token()

                if user:
                    raise Exception('Logout dulu untuk bisa melakukan register user')

                if len(data['password']) < 8:
                    raise Exception('password minimal 8 karakter')
                
                # Hash password dari user
                password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

                # Execute query
                cursor = mysql.connection.cursor()
                cursor.execute(
                    "CALL create_user(%s, %s, %s, %s)", 
                    (data['email'], data['fullname'], password, False)
                )

                cursor.close()
                return jsonify({"message": "User created"})
            except Exception as e:
                print(str(e))
                return make_response(jsonify({'message': 'error occured', 'error': str(e)}), 500)
        if user_type == 'admin':
            try:
                if len(data['password']) < 8:
                    raise Exception('password minimal 8 karakter')
                
                # Hash password dari user
                password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

                user = service.decode_jwt_token()

                if not user['role']:
                    return make_response({'message': 'kamu tidak bisa register admin baru'}, 403)

                # Execute query
                cursor = mysql.connection.cursor()
                cursor.execute(
                    "CALL create_user(%s, %s, %s, %s)", 
                    (data['email'], data['fullname'], password, True)
                )

                cursor.close()
                return jsonify({"message": "User created"})
            except Exception as e:
                print(str(e))
                return make_response(jsonify({'message': 'error occured', 'error': str(e)}), 500)
        else:
            return make_response(jsonify({'message': 'invalid parameter'}), 404)


    def delete(self):
        # data : email
        data = request.json
        try:
            email = data.get('email')

            user = service.decode_jwt_token()

            if not user['role']:
                return make_response(jsonify({'message': 'kamu tidak memiliki akses'}), 403)

            cursor = mysql.connection.cursor()
            query = "CALL hapus_user(%s)"
            cursor.execute(query, (email, ))
            cursor.close()

            return jsonify({ 'message': f'User dengan email {email} berhasil dihapus' })

        except Exception as e:
            return make_response(jsonify({'message': 'error occured', 'error': str(e)}), 500)
