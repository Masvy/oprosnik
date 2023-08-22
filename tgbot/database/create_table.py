from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger

BaseModel = declarative_base()


class User(BaseModel):
    __tablename__ = 'users'

    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)
