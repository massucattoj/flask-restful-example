from flask_jwt import jwt_required
from flask_restful import Resource, reqparse
from models.item import ItemModel


class Item(Resource): # Every resources need to be a class
    # Now Item is a copy of Resource with sth more.

    ''' Using parse to get just the fields that want update ,look to the json payload and get price for example '''
    parser = reqparse.RequestParser()
    parser.add_argument('price', type=float, required=True, help='This field cannot be left blank')
    parser.add_argument('store_id', type=int, required=True, help='Every item needs a store id')

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' item already exist.".format(name)}, 400

        data = Item.parser.parse_args()
        item = ItemModel(name, **data)

        try:
            item.save_to_db()
        except:
            return {"message": "An error ocurred inserting the item."}, 500 # Internal Server Error

        return item.json(), 201

    def put(self, name):
        data = Item.parser.parse_args()

        item = ItemModel.find_by_name(name)

        if item is None:
            item = ItemModel(name, data['price'], data['store_id'])
        else:
           item.price = data['price']
           item.store_id = data['store_id']

        item.save_to_db() # Save price with changes or create a new item with name was not found
        return item.json()  # updated_item is a ItemModel, need to be transformed into json

    def delete(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': "Item deleted"}


class ItemList(Resource):
    def get(self):
        #return {'items': [item.json() for item in ItemModel.query.all()] }
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}
