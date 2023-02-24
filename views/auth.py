from flask import request
from flask_restx import Resource, Namespace, abort

from implemented import auth_service

auth_ns = Namespace('auth')


@auth_ns.route('/register')
class AuthRegisterView(Resource):
    def post(self):
        req_json = request.get_json()
        email = req_json.get('email', None)
        password = req_json.get('password', None)

        if None in [email, password]:
            abort(400)

        auth_service.create_user(req_json)

        return '', 201


@auth_ns.route('/login')
class AuthLoginView(Resource):
    def post(self):
        req_json = request.get_json()
        email = req_json.get('email', None)
        password = req_json.get('password', None)

        if None in [email, password]:
            abort(400)

        tokens = auth_service.generate_tokens(email, password)

        return tokens, 201

    def put(self):
        req_json = request.get_json()
        refresh_token = req_json.get('refresh_token')
        if refresh_token is None:
            abort(400)

        tokens = auth_service.approve_refresh_token(refresh_token)

        return tokens, 201
