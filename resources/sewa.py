from flask_restful import Resource
from db import mysql
from flask import jsonify, request, make_response
from . import service
from datetime import datetime

class Sewa(Resource):
    def get(self):
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('CALL get_all_sewa()')
            rows = cursor.fetchall()
            data = service.cursor_to_json(cursor, rows)
            return jsonify({'message': 'sewa fetched', 'data': data})
        except Exception as e:
            return make_response(jsonify({'message': 'error occured', 'error': str(e)}), 500)


    def post(self):
        # URUTAN : PLAT, ID USER, TANGGAL MULAI, TANGGAL SELESAI
        data = request.json
        try:
            user = service.decode_jwt_token()

            if user['role']:
                return make_response(jsonify({'message': 'admin tidak boleh melakukan kegiatan sewa'}), 403)

            cursor = mysql.connection.cursor()

            cursor.execute("CALL sewa_kendaraan(%s, %s, %s, %s)", (data['plat_nomor'], user['id'], data['tanggal_mulai'], data['tanggal_selesai']))
            cursor.close()

            return jsonify({'message': f'Kendaraan Berhasil Disewa ({data["plat_nomor"]})'})

        except Exception as e:
            response = make_response(jsonify({'message': 'Error Occured', 'error': str(e)}), 500)
            return response
        
    def delete(self, id):
        try:
            user = service.decode_jwt_token()

            if not user['role']:
                return make_response(jsonify({'message': 'kamu tidak memiliki akses'}), 403)
            
            cursor = mysql.connection.cursor()
            cursor.execute('CALL hapus_sewa(%s)', (id, ))
            cursor.close()

            return jsonify({'message': 'data sewa berhasil dihapus'})

        except Exception as e:
            return make_response(jsonify({'message': 'error occured', 'error': str(e)}), 403)

        