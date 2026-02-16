from sqlalchemy import ForeignKey, BigInteger, Column, String, Numeric
from sqlalchemy.orm import relationship

from app.core.models import Base, IntIdMixin, TimeActionMixin


class Order(Base, IntIdMixin, TimeActionMixin):
    __tablename__ = 'orders'

    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    address = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    comment = Column(String(255), nullable=False)
    status = Column(String(30), nullable=False)

    order_products = relationship("OrderProducts", backref="order", lazy="selectin")


class OrderProduct(Base, IntIdMixin):
    __tablename__ = 'order_products'

    order_id = Column(BigInteger, ForeignKey('orders.id'), nullable=False)
    product_id = Column(BigInteger, ForeignKey('products.id'), nullable=False)
    quantity = Column(BigInteger, nullable=False, default=1)
    price = Column(Numeric(20, 2), nullable=False)

