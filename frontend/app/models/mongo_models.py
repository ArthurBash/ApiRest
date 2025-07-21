from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
import jwt
from flask import current_app

class MongoUser:
    def __init__(self, db):
        self.collection = db.users

    def create_user(self, user_data):
        user_data['created_at'] = datetime.utcnow()
        user_data['updated_at'] = datetime.utcnow()
        user_data['is_active'] = True
        user_data['role'] = 'user'
        return self.collection.insert_one(user_data)

    def get_user(self, user_id):
        return self.collection.find_one({'_id': ObjectId(user_id)})

    def get_user_by_username(self, username):
        return self.collection.find_one({'username': username})

    def get_user_by_email(self, email):
        return self.collection.find_one({'email': email})

    def update_user(self, user_id, update_data):
        update_data['updated_at'] = datetime.utcnow()
        return self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': update_data}
        )

    def delete_user(self, user_id):
        return self.collection.delete_one({'_id': ObjectId(user_id)})

    def set_password(self, user_id, password):
        hashed_password = generate_password_hash(password)
        return self.collection.update_one(
            {'_id': ObjectId(user_id)},
            {'$set': {'password_hash': hashed_password, 'updated_at': datetime.utcnow()}}
        )

    def check_password(self, user_id, password):
        user = self.get_user(user_id)
        if user and 'password_hash' in user:
            return check_password_hash(user['password_hash'], password)
        return False

    def generate_token(self, user_id, expires_in=3600):
        user = self.get_user(user_id)
        if user:
            return create_access_token(identity=str(user['_id']), expires_delta=expires_in)
        return None

    def as_dict(self, user):
        if user:
            return {
                'id': str(user['_id']),
                'username': user.get('username'),
                'email': user.get('email'),
                'created_at': user.get('created_at').isoformat(),
                'updated_at': user.get('updated_at').isoformat(),
                'is_active': user.get('is_active', True),
                'role': user.get('role', 'user')
            }
        return None

def insert_user_mongo(data):
    mongo_users = current_app.mongo_client["users_mongo"]
    return mongo_users.insert_one(data)

def get_user_mongo_by_username(username):
    mongo_users = current_app.mongo_client["users_mongo"]
    return mongo_users.find_one({"username": username})

def list_users_mongo():
    mongo_users = current_app.mongo_client["users_mongo"]
    return list(mongo_users.find({}, {"_id": 0}))

def delete_user_mongo(username):
    mongo_users = current_app.mongo_client["users_mongo"]
    return mongo_users.delete_one({"username": username})
