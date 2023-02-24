import calendar
import datetime

import jwt
from flask_restx import abort

from helpers.constants import JWT_SECRET, JWT_ALGO
from service.users import UserService


class AuthService:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def generate_tokens(self, email, password, is_refresh=False):
        user = self.user_service.get_by_email(email)

        if user is None:
            abort(404)

        if not is_refresh:
            if not self.user_service.compare_passwords(user.password, password):
                abort(400)

        data = {
            'email': user.email,
            'password': str(user.password)
        }

        min30 = datetime.datetime.utcnow() + datetime.timedelta(minutes=30)
        data["exp"] = calendar.timegm(min30.timetuple())
        access_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        days130 = datetime.datetime.utcnow() + datetime.timedelta(days=130)
        data["exp"] = calendar.timegm(days130.timetuple())
        refresh_token = jwt.encode(data, JWT_SECRET, algorithm=JWT_ALGO)

        tokens = {"access_token": access_token, "refresh_token": refresh_token}

        return tokens

    def approve_refresh_token(self, refresh_token):
        try:
            data = jwt.decode(refresh_token, JWT_SECRET, algorithms=[JWT_ALGO])
        except Exception as e:
            print(e)
            abort(400)

        email = data.get('email')

        return self.generate_tokens(email, None, is_refresh=True)

    def create_user(self, data):
        self.user_service.create(data)
