from flask import Blueprint
from flask import current_app as app
from flask import jsonify
from flask import request
from flask import abort
import jwt

from app.custom_exceptions import InvalidAuthorizationException, UserNotFoundException, IncorrectPasswordException
from app.methods import Auth, JWTToken, Restricted

authentication = Auth()
jwt_token = JWTToken()
protected = Restricted()

bp_app_routes = Blueprint("main", __name__)

# Just a health check


@bp_app_routes.route("/")
def url_root():
    return "OK"


# Just a health check
@bp_app_routes.route("/_health")
def url_health():
    return "OK"


# e.g. http://127.0.0.1:8000/login
@bp_app_routes.route("/login", methods=['POST'])
def url_login():
    username = request.form['username']
    password = request.form['password']

    responseBody = {'data': {}, 'code': 200}

    try:
        user = authentication.authenticateUser(username, password)
        jwt_token_generated = jwt_token.generate_token(user.role)
        responseBody['data'] = {
            'token': jwt_token_generated
        }
    except UserNotFoundException as ex:
        app.logger.exception(ex)
        responseBody['code'] = 403
        responseBody['data'] = {
            'error': 'Authentication failed. The username or password are incorrect.'
        }
        abort(403, responseBody)
    except IncorrectPasswordException as ex:
        app.logger.exception(ex)
        responseBody['code'] = 403
        responseBody['data'] = {
            'error': 'Authentication failed. The username or password are incorrect.'
        }
        abort(403, responseBody)
    except Exception as ex:
        app.logger.exception(ex)
        abort(500)

    return jsonify(responseBody)


# # e.g. http://127.0.0.1:8000/protected
@bp_app_routes.route("/protected")
def url_protected():

    responseBody = {'data': {}, 'code': 200}

    try:
        auth_token = request.headers.get('Authorization')
        has_access = protected.has_access_data(auth_token)
        responseBody['data'] = {
            'has_access': has_access
        }
    except InvalidAuthorizationException as ex:
        app.logger.exception(ex)
        responseBody['code'] = 401
        responseBody['data'] = {
            'error': 'Invalid authorization header.'
        }
        abort(401, responseBody)
    except jwt.InvalidSignatureError as ex:
        app.logger.exception(ex)
        responseBody['code'] = 401
        responseBody['data'] = {
            'error': 'Token has expired or is invalid.'
        }
        abort(401, responseBody)
    except Exception as ex:
        app.logger.exception(ex)
        abort(500)

    return jsonify(responseBody)
