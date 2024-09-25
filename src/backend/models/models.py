from datetime import datetime
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Float
from src.database import Base


class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=False)
    price = Column(Float, nullable=False)
    quantity_on_hand = Column(Integer, default=0, nullable=False)


class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)
    created_date = Column(TIMESTAMP, default=datetime.utcnow)
    status = Column(String, nullable=False, default="в процессе")


class OrderItem(Base):
    __tablename__ = "order_item"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("product.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
