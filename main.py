from flask import Flask
from flask_restful import Api
from db import mysql
from resources.user import User
from resources.auth import Login
from resources.kendaraan import Kendaraan
from resources.tipe_kendaraan import TipeKendaraan
from resources.sewa import Sewa
from resources.kembali import Kembali
from resources.history import History


app = Flask(__name__)
api = Api(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'flaskdb'

mysql.init_app(app)

api.add_resource(User, '/users/')
api.add_resource(Login, '/auth/login/')
api.add_resource(Kendaraan, '/kendaraan/')
api.add_resource(Sewa, '/sewa/')
api.add_resource(Kembali, '/kembali/')
api.add_resource(History, '/history/<string:history_type>/')


if __name__ == '__main__':
    app.run(debug=True)