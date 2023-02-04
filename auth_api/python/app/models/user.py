from extensions import db


class User(db.Model):
    __tablename__ = "users"
    username = db.Column(db.Text, primary_key=True)
    password = db.Column(db.Text)
    salt = db.Column(db.Text)
    role = db.Column(db.Text)

    def __repr__(self):
        return f'<User {self.content}>'
