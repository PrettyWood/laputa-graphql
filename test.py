import enum
from datetime import datetime

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from sqlalchemy import Column, Enum, Integer, String, ForeignKey, DateTime, Boolean, ARRAY

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///laputa.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class RoleEnum(enum.Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'
    SUPER_ADMIN = 'SUPER ADMIN'


class PrivilegeEnum(enum.Enum):
    NONE = 'none'
    VIEW = 'view'
    CONTRIBUTE = 'contribute'


class SmallApp(db.Model):
    _id = Column(Integer, primary_key=True)
    id = Column(String(100), unique=True, nullable=False)
    name = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.id!r}>'


class Group(db.Model):
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f'<User {self.name!r}>'


class Privilege(db.Model):
    id = Column(Integer, primary_key=True)
    user = Column(Integer, ForeignKey('user.id'), nullable=False)
    small_app = Column(Integer, ForeignKey('small_app.id'), nullable=False)
    privilege = Column(Enum(PrivilegeEnum, values_callable=lambda x: [e.value for e in x]),
                       default=PrivilegeEnum.NONE)


class User(db.Model):
    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    created_by = Column(Integer, ForeignKey('user.id'), nullable=True)
    creation_date = Column(DateTime, nullable=False, default=datetime.utcnow)
    expiration_date = Column(DateTime)
    password_email_sent = Column(Boolean, default=False)
    logins = Column(ARRAY(DateTime))
    groups = Column(ARRAY(Integer, ForeignKey('group.id')))
    role = Column(Enum(RoleEnum, values_callable=lambda x: [e.value for e in x]),
                  default=RoleEnum.USER)

    def __repr__(self):
        return f'<User {self.username!r}>'
