from flask_restful import Resource
from db import mysql
from flask import jsonify, request, make_response
from . import service

class Kendaraan(Resource):
    def get(self):
        try:
            cursor = mysql.connection.cursor()
            cursor.execute('CALL get_all_kendaraan()')
            rows = cursor.fetchall()
            data = service.cursor_to_json(cursor, rows)
            return jsonify({'message': 'kendaraan fetched', 'kendaraan': data})

        except Exception as e:
            return make_response(jsonify({'message': 'error occured', 'error': str(e)}), 500)

    def post(self):
        # URUTAN : PLAT, HARGA TIPE
        data = request.json
        try:
            cursor = mysql.connection.cursor()

            user = service.decode_jwt_token()

            if not user['role']:
                return jsonify({ "message":"Kamu tidak memiliki akses" })

            # Execute query
            cursor.execute("CALL tambah_kendaraan(%s, %s, %s)", (data['plat_nomor'], data['harga_per_hari'], data['tipe']))
            cursor.close()

            return jsonify({'message': f'Kendaraan ditambahkan ({data['plat_nomor']})'})
        except Exception as e:
            return make_response(jsonify({'message': 'error occured', 'error': str(e)}), 500)


    def put(self):
        data = request.json
        try:
            cursor = mysql.connection.cursor()
            cursor.execute("CALL update_kendaraan(%s, %s)", (data['plat_nomor'], data['harga_baru']))
            cursor.close()

            return jsonify({'message': f'Kendaraan dengan plat nomor {data['plat_nomor']} berhasil diupdate'})
        except Exception as e:
            return make_response(jsonify({'message': 'error occured', 'error': str(e)}), 500)

    def delete(self):
        # INPUT : PLAT
        try:
            user = service.decode_jwt_token()

            print(user)

            if not user['role']:
                return jsonify({ "message":"Kamu tidak memiliki akses" })
            
            data = request.json
            cursor = mysql.connection.cursor()

            # Execute query
            cursor.execute("CALL hapus_kendaraan(%s)", (data['plat_nomor'],))
            cursor.close()

            return jsonify({'message': f'Kendaraan dengan plat nomor {data['plat_nomor']} berhasil dihapus'})
        except Exception as e:
            return make_response(jsonify({'message': 'error occured', 'error': str(e)}), 500)