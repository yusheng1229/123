from sqlalchemy import Column, Integer, String, ForeignKey, REAL
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    user_id = Column(String, primary_key=True)
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    orders = relationship("Order", backref="user", cascade="all, delete-orphan")


class Order(Base):
    __tablename__ = "orders"
    order_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, ForeignKey("users.user_id"))
    order_list = Column(String)
    total_amount = Column(REAL)