from flask_restful import Resource
from db import mysql
from flask import jsonify, request
from . import service

class Sewa(Resource):
    def post(self):
        # URUTAN : PLAT, ID USER, TANGGAL MULAI, TANGGAL SELESAI
        data = request.json

        print(data)

        cursor = mysql.connection.cursor()

        user = service.decode_jwt_token()

        print(user)

        # Get price for the car
        cursor.execute("CALL sewa_kendaraan(%s, %s, %s, %s)", (data['plat_nomor'], user['id'], data['tanggal_mulai'], data['tanggal_selesai']))
        row = cursor.fetchone()
        cursor.close()

        return jsonify({'message': 'Kendaraan Berhasilar', 'data': row})