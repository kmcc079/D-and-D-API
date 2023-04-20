from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets

# set variables for class instantiation
login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(150), nullable=False, unique=True)
    password = db.Column(db.String, nullable=True, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True )
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__(self, username, email, password='', token='', g_auth_verify=False):
        self.id = self.set_id()
        self.username = username
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.username} has been added!'
    

class Character(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    race = db.Column(db.String, nullable=False)
    _class = db.Column(db.String, nullable=False)
    alignment = db.Column(db.String, nullable=False)
    background = db.Column(db.String, nullable=False)
    level = db.Column(db.Integer, nullable=False)
    experience = db.Column(db.Integer, nullable=False)
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, name, race, _class, alignment, background, level, experience, user_token, id=''):
        self.id = self.set_id()
        self.name = name
        self.race = race
        self._class = _class
        self.alignment = alignment
        self.background = background
        self.level = level
        self.experience = experience
        self.user_token = user_token

    def __repr__(self):
        return f'The following character has been added to your list: {self.name} - Level {self.level} {self.race} {self._class}'
    
    def set_id(self):
        return secrets.token_urlsafe()
    
class CharSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'race', '_class', 'alignment', 'background', 'level', 'experience']

char_schema = CharSchema()
charas_schema = CharSchema(many=True)