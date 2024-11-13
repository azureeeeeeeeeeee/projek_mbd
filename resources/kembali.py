from flask_restful import Resource
from db import mysql
from flask import jsonify, request
from . import service

class Kembali(Resource):
    def post(self):
        # URUTAN : PLAT, TANGGAL KEMBALI, RUSAK, METODE_PEMBAYARAN
        data = request.json

        cursor = mysql.connection.cursor()

        user = service.decode_jwt_token()

        print(user)

        # Executing procedure
        cursor.execute("CALL kembalikan_kendaraan(%s, %s, %s, %s)", (data['plat_nomor'], data['tanggal_kembali'], data['kondisi'], data['metode_pembayaran']))
        row = cursor.fetchone()
        cursor.close()

        return jsonify({'message': f'Berhasil mengembalikan kendaraan {data['plat_nomor']}', 'data': row})