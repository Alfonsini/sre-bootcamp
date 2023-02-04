from flask import current_app as app
from app.models.user import User

# These functions need to be implemented
class UserRepository:

    def getUserByUsername(self, username):
        user = None

        try:
            user = User.query.filter_by(username=username).first()
        except Exception as ex:
            app.logger.exception(ex)
    
        return user