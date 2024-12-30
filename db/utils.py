from .database import get_db
from .models import Order
from typing import Generator
from sqlalchemy.orm import Session

def save_order(user_id:str, items:str, total_price:int) :
    with next(get_db()) as session :
        order = Order(user_id=user_id, items=items, total_price=total_price)
        session.add(order)
        session.commit()

def get_order_by_user_id(user_id:str) :
    with next(get_db()) as session :
        order = session.query(Order).filter_by(user_id=user_id).first()
        return order