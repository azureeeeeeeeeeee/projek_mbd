from flask_restful import Resource
from db import mysql
from flask import jsonify, request, make_response
from . import service

class TipeKendaraan(Resource):
    def get(self):
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('CALL get_all_tipe()')
            rows = cursor.fetchall()
            data = service.cursor_to_json(cursor, rows)
            return jsonify({'message': 'tipe kendaraan berhasil difetch', 'users': data})

        except Exception as e:
            return make_response(jsonify({'message': 'error occured', 'error': str(e)}), 500)


    def delete(self):
        # data -> tipe

        try:
            data = request.json
            tipe = data.get('tipe')

            user = service.decode_jwt_token()


            if not user['role']:
                return make_response({'message':"you are not authorized"}, 403)
            cursor = mysql.connection.cursor()
            cursor.execute('CALL hapus_tipe_kendaraan(%s)', (tipe, ))
            cursor.close()

            return jsonify({'message': f'Tipe Kendaraan {tipe} berhasil dihapus'})
        except Exception as e:
            response = make_response(jsonify({'message':'error occured', "error":str(e)}), 500)
            return response