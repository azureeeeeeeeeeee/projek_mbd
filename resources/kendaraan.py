from flask_restful import Resource
from db import mysql
from flask import jsonify, request
from . import service

class Kendaraan(Resource):
    def post(self):
        # URUTAN : PLAT, HARGA TIPE
        data = request.json
        cursor = mysql.connection.cursor()

        # Execute query
        cursor.execute("CALL tambah_kendaraan(%s, %s, %s)", (data['plat_nomor'], data['harga_per_hari'], data['tipe']))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': f'Kendaraan ditambahkan ({data['plat_nomor']})'})
    
    def delete(self):
        # INPUT : PLAT

        user = service.decode_jwt_token()

        print(user)

        if not user['role']:
            return jsonify({ "message":"Kamu tidak memiliki akses" })
        
        data = request.json
        cursor = mysql.connection.cursor()

        # Execute query
        cursor.execute("CALL hapus_kendaraan(%s)", (data['plat_nomor'],))
        mysql.connection.commit()
        cursor.close()

        return jsonify({'message': f'Kendaraan dengan plat nomor {data['plat_nomor']} berhasil dihapus'})