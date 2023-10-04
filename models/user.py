#!/usr/bin/python3
""" holds class User"""

import hashlib
import models
from models.base_model import BaseModel, Base
from os import getenv
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
        super().__init__(*args, **kwargs)
        print(self.password)
        pwd = self.hash_password(self.password)
        setattr(self, "password", pwd)

    def hash_password(self, password):
        """Hashes the password using Md5 hashing algorithm"""
        md5 = hashlib.md5()

        md5.update(password.encode('utf-8'))
        return md5.hexdigest()
