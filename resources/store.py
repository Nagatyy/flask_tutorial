from flask_restful import Resource
from models.store import StoreModel
from flask_jwt import jwt_required


class Store(Resource):

    @jwt_required()
    def get(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            return store.json()
        return {'message': 'Store not found'}, 404

    @jwt_required()
    def post(self, name):
        if StoreModel.find_by_name(name):
            return {'message': f"An store with name '{name}' already exists."}, 400

        store = StoreModel(name)

        try:
            store.save_to_db()
        except:
            return {'message': f"Failed to save store to database"}, 500
        
        return store.json(), 201

    @jwt_required()
    def delete(self, name):
        store = StoreModel.find_by_name(name)

        if store:
            store.delete_from_db()
        
        return {'message': 'Store deleted'}

class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in StoreModel.find_all()]}

