import os

from sqlalchemy import BigInteger, String
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import StringEncryptedType

from .Base import Base


SECRET = os.getenv('SECRET').encode()

class User(Base):
    __tablename__ = "Users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)

    # Credentials
    api_key: Mapped[str] = mapped_column(StringEncryptedType(String, SECRET), nullable=True)