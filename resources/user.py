import sqlite3
from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import create_access_token, create_refresh_token


class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        data = UserRegister.parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "User with that username already exists."}, 400

        # user = UserModel(data['username'], data['password']])
        user = UserModel(**data)
        user.save_to_db()

        return {"message": "User created successfully."}, 201

class User(Resource):

    def get(self, user_id):
        user = UserModel.find_by_id(user_id)

        if not user:
            return {'message': 'user not found'}, 400

        return user.json()

    def delete(self, user_id):
        user = UserModel.find_by_id(user_id)

        if user:
            user.delete_from_db()
        
        
        return {'message': 'user has been deleted'}

# to do exactly what /auth did before
class UserLogin(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )
    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="This field cannot be left blank!"
                        )

    def post(self):
        # get data from parser
        data = self.parser.parse_args()
        # find user in database
        user = UserModel.find_by_username(data['username'])
        # check password
        if user and safe_str_cmp(data['password'], user.password):
            
            # create and return access and refresh token
            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)

            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        
        return {'message': 'Invalid credentials'}, 401