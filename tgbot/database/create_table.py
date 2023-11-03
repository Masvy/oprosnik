from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, BigInteger, VARCHAR

BaseModel = declarative_base()


class User(BaseModel):
    __tablename__ = 'users'

    user_id = Column(BigInteger, unique=True, nullable=False, primary_key=True)

    first_name = Column(VARCHAR(64), unique=False, nullable=False)

    user_name = Column(VARCHAR(32), unique=True, nullable=True)

    def __repr__(self):
        return f"<User(user_id={self.user_id}, first_name={self.first_name}, user_name={self.user_name})>"
