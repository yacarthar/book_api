import re

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import validates

from ..libs.db import Base
from ..libs.security import pwd_context


class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(30), unique=True, index=True)
    email = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(64))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)

    @validates("email")
    def validate_email(self, key, email):
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email address")
        return email

    def set_password(self, password):
        self.hashed_password = pwd_context.hash(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.hashed_password)
