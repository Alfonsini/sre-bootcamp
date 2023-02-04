

class UserNotFoundException(Exception):
    ...
    pass

class IncorrectPasswordException(Exception):
    ...
    pass

class JWTSecretKeyNotFoundException(Exception):
    ...
    pass

class InvalidAuthorizationException(Exception):
    ...
    pass