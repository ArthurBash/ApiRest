from flask import jsonify, request
from app.services.user_service import UserService

class UserController:
    @staticmethod
    def create_user():
        data = request.get_json()
        user, error, status_code = UserService.create_user(data)
        if error:
            return jsonify({'error': error}), status_code
        return jsonify(user.to_dict()), 201

    @staticmethod
    def get_all_users():
        users = UserService.get_all_users()
        return jsonify([user.to_dict() for user in users]), 200

    @staticmethod
    def get_user(user_id):
        user = UserService.get_user_by_id(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        return jsonify(user.to_dict()), 200

    @staticmethod
    def update_user(user_id):
        data = request.get_json()
        user, error, status_code = UserService.update_user(user_id, data)
        if error:
            return jsonify({'error': error}), status_code
        return jsonify(user.to_dict()), 200

    @staticmethod
    def delete_user(user_id):
        user, error, status_code = UserService.delete_user(user_id)
        if error:
            return jsonify({'error': error}), status_code
        return jsonify({'message': 'Usuario eliminado'}), 200