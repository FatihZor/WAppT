from mongoengine import connect, CASCADE, StringField, ReferenceField, IntField, ListField, Document, DictField, DateTimeField
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

connect('wapptV1')

class Users(UserMixin, Document):
    name = StringField()
    email = StringField()
    username = StringField(unique=True)
    password = StringField()
    user_type = StringField()