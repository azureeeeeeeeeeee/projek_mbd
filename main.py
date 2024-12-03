from flask import Flask
from flask_restful import Api
from db import mysql
from resources.user import User
from resources.auth import Login, Logout
from resources.kendaraan import Kendaraan
from resources.tipe_kendaraan import TipeKendaraan
from resources.sewa import Sewa
from resources.kembali import Kembali
from resources.history import History


app = Flask(__name__)
api = Api(app)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'mbd'
app.config['MYSQL_PASSWORD'] = 'mbd123'
app.config['MYSQL_DB'] = 'flaskdb'

mysql.init_app(app)

api.add_resource(User, '/users/', '/users/<string:user_type>')
api.add_resource(Login, '/auth/login/')
api.add_resource(Logout, '/auth/logout/')
api.add_resource(Kendaraan, '/kendaraan/')
api.add_resource(TipeKendaraan, '/kendaraan/tipe/')
api.add_resource(Sewa, '/sewa/', '/sewa/<int:id>/')
api.add_resource(Kembali, '/kembali/')
api.add_resource(History, '/history/<string:history_type>/')


if __name__ == '__main__':
    for rule in app.url_map.iter_rules():
        print(f"{rule.endpoint}: {rule.methods} {rule}")
    app.run(debug=True)