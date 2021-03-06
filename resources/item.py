from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt
from models.items import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help="This field cannot be left blank!"
    )

    parser.add_argument('store_id',
        type=int,
        required=True,
        help="Every item needs a store id!"
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404


    def post(self, name):
        if ItemModel.find_by_name(name):
            return {'message': "An item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()

        item = ItemModel(name, data['price'], data['store_id'])

        try:
            item.save_to_db()
        except:
            return {"message": "An error occurred inserting the item."}, 500

        return item.json()


    @jwt_required()
    def delete(self, name):

        # automatically extracts any claims that came in with the jwt
        claims = get_jwt()
        # we want only admins to be able to delete items so:
        if not claims['is_admin']:
            return {'message': 'Admin privelage required'}, 404


        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message': 'Item deleted'}
     
    @jwt_required()
    def put(self, name):
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)

        # if the item does not exist, insert it. If it exists, update it
        if item:
            item.price = data['price']
        else:
            item = ItemModel(name, data['price'], data['store_id'])
        item.save_to_db()
                
        return item.json()

    
class ItemList(Resource):

    def get(self):
        return {'items': [item.json() for item in ItemModel.find_all()]}

        
