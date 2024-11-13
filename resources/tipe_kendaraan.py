from flask_restful import Resource
from db import mysql
from flask import jsonify, request

class TipeKendaraan(Resource):
    def get(self, id=None):
        cursor = mysql.connection.cursor()
        data = request.json

        cursor.execute('CALL get_or_create_tipe_kendaraan(%s)', (data['tipe'],))
        row = cursor.fetchone()
        cursor.close()

        print(row)

        return jsonify({'message': f'Tipe Kendaraan {data['tipe']}'})