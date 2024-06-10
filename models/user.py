#!/usr/bin/python3
""" holds class User"""
import models
import hashlib
from models.base_model import BaseModel, Base
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        if 'password' in kwargs:
            kwargs['password'] = hashlib.md5(kwargs['password'].
                                             encode('utf8')).hexdigest()
        super().__init__(*args, **kwargs)

    def __setattr__(self, name, value):
        """hash the password and set other attributes"""
        if name == 'password' and isinstance(value, str):
            value = hashlib.md5(value.encode('utf8')).hexdigest()
        super().__setattr__(name, value)
