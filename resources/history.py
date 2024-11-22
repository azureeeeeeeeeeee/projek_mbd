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
            rows = cursor.fetchall()

            columns = [column[0] for column in cursor.description]
            print(columns)
            history = [dict(zip(columns, row)) for row in rows]

            cursor.execute('CALL get_total_revenue_procedure(%s)', (plat_nomor,))
            total_revenue = cursor.fetchone()[0]

            cursor.close()

            return jsonify({"message": f"Berhasil fetch history kendaraan ({plat_nomor})", "history": history, "total_revenue": total_revenue})
        
        elif history_type == 'user':
            user = service.decode_jwt_token()
            cursor.execute('CALL get_sewa_history_user(%s)', (user['id'],))
            rows = cursor.fetchall()

            columns = [column[0] for column in cursor.description]
            print(columns)
            history = [dict(zip(columns, row)) for row in rows]

            cursor.execute('CALL get_total_revenue_user_procedure(%s)', (user['id'],))
            total_revenue = cursor.fetchone()[0]

            cursor.close()

            return jsonify({"message": f"Berhasil fetch history user (id: {user['id']})", "history": history, "total_revenue": total_revenue})
        
        else:
            return jsonify({"message": "Invalid parameter"})