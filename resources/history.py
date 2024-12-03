from flask_restful import Resource
from db import mysql
from flask import jsonify, request, make_response
from . import service

class History(Resource):
    def post(self, history_type):
        cursor = mysql.connection.cursor()
        if history_type == 'kendaraan':
            try:
                user = service.decode_jwt_token()


                if not user['role']:
                    raise Exception('Kamu tidak memiliki akses')

                plat_nomor = request.json['plat_nomor']
                cursor.execute('CALL get_sewa_history_kendaraan(%s)', (plat_nomor,))
                rows = cursor.fetchall()

                history = service.cursor_to_json(cursor, rows)

                cursor.execute('CALL get_total_revenue_procedure(%s)', (plat_nomor,))
                total_revenue = cursor.fetchone()[0]

                cursor.close()

                return jsonify({"message": f"Berhasil fetch history kendaraan ({plat_nomor})", "history": history, "total_revenue": total_revenue})
            except Exception as e:
                return make_response(jsonify({'message': 'error occured', 'error': str(e)}), 500)


        elif history_type == 'user':
            try:
                user = service.decode_jwt_token()

                if not user['role']:
                    cursor.execute('CALL get_sewa_history_user(%s)', (user['id'],))
                    rows = cursor.fetchall()

                    history = service.cursor_to_json(cursor, rows)

                    cursor.execute('CALL get_total_revenue_user_procedure(%s)', (user['id'],))
                    total_revenue = cursor.fetchone()[0]

                    cursor.close()

                    return jsonify({"message": f"Berhasil fetch history user (id: {user['id']})", "history": history, "total_revenue": total_revenue})
                

                else:
                    email = request.json.get('email')

                    
                    if not email:
                        raise Exception('Sebagai admin, email wajib disertakan dalam request body')

                    cursor.execute('CALL get_sewa_history_user_by_email(%s)', (email, ))
                    rows = cursor.fetchall()

                    history = service.cursor_to_json(cursor, rows)

                    cursor.execute('CALL get_total_revenue_user_procedure(%s)', (user['id'],))
                    total_revenue = cursor.fetchone()[0]

                    cursor.close()

                    return jsonify({"message": f"Berhasil fetch history user (id: {user['id']})", "history": history, "total_revenue": total_revenue})

            except Exception as e:
                return make_response(jsonify({'message': 'error occured', 'error': str(e)}), 500)
        
        else:
            return jsonify({"message": "Invalid parameter"})