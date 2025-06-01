from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship, declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True)
    password = Column(String, nullable=False)
    poosey = relationship(
        "Password", back_populates="user", cascade="all , delete-orphan"
    )


class Password(Base):
    __tablename__ = "passwords"
    id = Column(Integer, autoincrement=True, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String, nullable=False)
    login = Column(String, nullable=False)
    passwd = Column(String, nullable=False)
    user = relationship("User", back_populates="poosey")
