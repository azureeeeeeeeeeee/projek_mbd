from flask_restful import Resource
from db import mysql
from flask import jsonify, request, make_response
from . import service

class Kembali(Resource):
    def post(self):
        # URUTAN : PLAT, TANGGAL KEMBALI, RUSAK, METODE_PEMBAYARAN
        data = request.json

        try:

            cursor = mysql.connection.cursor()

            user = service.decode_jwt_token()

            if not user['role']:
                return make_response({'message': 'kamu tidak memiliki akses'}, 403)


            # Executing procedure
            cursor.execute("CALL kembalikan_kendaraan(%s, %s, %s, %s)", (data['plat_nomor'], data['tanggal_kembali'], data['rusak'], data['metode_pembayaran']))
            row = cursor.fetchone()
            cursor.close()

            return jsonify({'message': f'Berhasil mengembalikan kendaraan {data['plat_nomor']}', 'total': row[0]})
        except Exception as e:
            return make_response(jsonify({'message': 'error occured', 'error': str(e)}), 500)