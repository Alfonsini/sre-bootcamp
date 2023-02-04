from flask import current_app as app
from app.repositories.userRepository import UserRepository
import hashlib
import jwt
from app.config.config import Config

from app.custom_exceptions import InvalidAuthorizationException, UserNotFoundException, IncorrectPasswordException, JWTSecretKeyNotFoundException

# These functions need to be implemented

userRepository = UserRepository()


class Auth:
    def authenticateUser(self, username, password):
        user = userRepository.getUserByUsername(username)

        if user == None:
            raise UserNotFoundException()

        generated_password = self._createPassword(password, user.salt)

        if generated_password != user.password:
            raise IncorrectPasswordException()

        return user

    def _createPassword(self, password, salt):
        saltedPassword = password+salt
        return hashlib.sha512(saltedPassword.encode()).hexdigest()


class JWTToken:

    def generate_token(self, userRole):

        if Config.JWT_SECRET_KEY == None:
            raise JWTSecretKeyNotFoundException()

        return jwt.encode({"role": userRole}, Config.JWT_SECRET_KEY, algorithm="HS256")


class Restricted:

    def has_access_data(self, authorization):
        has_access = False

        if 'Bearer' not in authorization:
            raise InvalidAuthorizationException()

        jwt_token = authorization.split()[1]

        payload = jwt.decode(jwt_token, Config.JWT_SECRET_KEY,
                   algorithms="HS256", options={"verify_signature": True})
        
        has_access = True

        return has_access
