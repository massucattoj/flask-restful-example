from datetime import timedelta

from flask import Flask
from flask_jwt import JWT
from flask_restful import Api

from db import db
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from resources.user import UserRegister
from security import authenticate, identity

''' Resource represents sth that the api represents -> items, students and so on...'''
''' We dont need to use jsonify with restful api, that happens automatically '''

app = Flask(__name__)
app.config['DEBUG'] = True

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db' # tell where is the database
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # specify configuration property
app.secret_key = 'bumblebee'
api = Api(app)

@app.before_first_request
def create_tables():
    db.create_all()

''' JWT creates a new endpoint # /auth '''
app.config['JWT_AUTH_URL_RULE'] = '/login' # changes /auth for /login
app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=1800)  # set expiration time to 30 min
jwt = JWT(app, authenticate, identity)


# Tell to the api the student is accessible via API
# And tell the url to access that ex: http://127.0.0.1:5000/item/
api.add_resource(Store, '/store/<string:name>')
api.add_resource(Item, '/item/<string:name>')
api.add_resource(UserRegister, '/register')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')

if __name__ == '__main__':
    from db import db
    db.init_app(app)

    if app.config['DEBUG']:
        @app.before_first_request
        def create_tables():
            db.create_all()

    app.run(port=5000)
