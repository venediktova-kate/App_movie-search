import jwt
from flask import request
from flask_restx import Resource, Namespace, abort

from dao.model.user import UserSchema
from helpers.constants import JWT_SECRET, JWT_ALGO
from helpers.decorators import auth_required
from implemented import user_service

user_ns = Namespace('user')


@user_ns.route('/')
class UsersView(Resource):
    @auth_required
    def get(self):
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        email = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO]).get('email')
        user = user_service.get_by_email(email)
        res = UserSchema().dump(user)
        del res['password']

        return res, 200

    @auth_required
    def patch(self):
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        email = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO]).get('email')
        req_json = request.json
        user_service.update(req_json, email)
        return "", 201

    @auth_required
    def put(self):
        data = request.headers['Authorization']
        token = data.split('Bearer ')[-1]
        email = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGO]).get('email')
        user = user_service.get_by_email(email)
        req_json = request.json

        if not user_service.compare_passwords(user.password, req_json.get('password_1')):
            abort(400)

        user.password = req_json.get('password_2')
        user_service.update_password(UserSchema().dump(user), email)

        return '', 201
