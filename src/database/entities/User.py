import os

from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import Mapped
from sqlalchemy_utils import StringEncryptedType

from .Base import Base


SECRET = os.getenv('SECRET').encode()

class User(Base):
    __tablename__ = "Users"

    id: Mapped[int] = Column(BigInteger, primary_key=True)
    api_key: Mapped[str] = Column(StringEncryptedType(String, SECRET), nullable=True)