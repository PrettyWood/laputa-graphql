import enum

import re
from sqlalchemy import Column, DateTime, Integer, String, func, ForeignKey, Boolean, Enum, Table
from sqlalchemy.orm import relationship, backref, validates

from database import Base

EMAIL_REGEX = r'(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)'


class Stage(enum.Enum):
    STAGING = 'staging'
    PRODUCTION = 'production'


class Role(enum.Enum):
    USER = 'USER'
    ADMIN = 'ADMIN'
    SUPER_ADMIN = 'SUPER ADMIN'


class PrivilegeEnum(enum.Enum):
    NONE = 'none'
    VIEW = 'view'
    CONTRIBUTE = 'contribute'


class SmallApp(Base):
    __tablename__ = 'smallapp'
    id = Column(String(100), primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    staging_last_update = Column(DateTime)
    production_last_update = Column(DateTime)

    def __repr__(self):
        return f'<SmallApp {self.id!r}>'


association_table = Table('user_usergroup', Base.metadata,
                          Column('user_id', Integer, ForeignKey('user.id')),
                          Column('usergroup_id', Integer, ForeignKey('usergroup.id'))
                          )


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    created_by_id = Column(Integer, ForeignKey('user.id'))
    created_users = relationship('User', backref=backref('created_by', remote_side=[id]))
    creation_date = Column(DateTime, default=func.now())
    expiration_date = Column(DateTime, nullable=True)
    password_email_sent = Column(Boolean, default=False)
    # logins = Column(ARRAY(DateTime))
    groups = relationship('Group', secondary=association_table, back_populates='users')
    role = Column(Enum(Role), default=Role.USER)

    @validates('name')
    def validate_isemail_name(self, key, name):
        assert re.match(EMAIL_REGEX, name) is not None
        return name

    def __repr__(self):
        return f'<User {self.name!r}>'


class Group(Base):
    __tablename__ = 'usergroup'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)
    users = relationship('User', secondary=association_table, back_populates='groups')

    def __repr__(self):
        return f'<Group {self.name!r}>'


class Privilege(Base):
    __tablename__ = 'privilege'
    id = Column(Integer, primary_key=True)
    # user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    # small_app_id = Column(Integer, ForeignKey('small_app.id'), nullable=False)
    # role = Column(Enum(PrivilegeEnum), default=PrivilegeEnum.NONE)
    # lambda x: [e.value for e in x]
    # def __repr__(self):
    #     return f'<Privilege {self.user_id!r}, {self.small_app_id!r}, {self.role!r}>'
