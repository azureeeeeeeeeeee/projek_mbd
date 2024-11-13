from flask_restful import Resource
from db import mysql
from flask import jsonify, request
from . import service

class History(Resource):
    def post(self, history_type):
        cursor = mysql.connection.cursor()
        if history_type == 'kendaraan':
            plat_nomor = request.json['plat_nomor']
            cursor.execute('CALL get_sewa_history_kendaraan(%s)', (plat_nomor,))
            row = cursor.fetchall()

            cursor.execute('SELECT get_total_revenue_by_kendaraan(%s)', (plat_nomor,))
            total_revenue = cursor.fetchone()[0]

            cursor.close()

            return jsonify({"message": f"Berhasil fetch history kendaraan ({plat_nomor})", "history": row, "total_revenue": total_revenue})
        
        elif history_type == 'user':
            data = request.json
            return jsonify({"message": "Retrieved user history"})
        
        else:
            return jsonify({"message": "Invalid parameter"})