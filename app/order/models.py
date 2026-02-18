from sqlalchemy import ForeignKey, BigInteger, Column, String, Numeric, UniqueConstraint, select, func
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import relationship

from app.core.models import Base, IntIdMixin, TimeActionMixin


class Order(Base, IntIdMixin, TimeActionMixin):
    __tablename__ = 'orders'

    user_id = Column(BigInteger, ForeignKey('users.id'), nullable=False)
    address = Column(String(255), nullable=False)
    phone_number = Column(String(20), nullable=False)
    comment = Column(String(255), nullable=False)
    status = Column(String(30), nullable=False)

    products = relationship("OrderProduct", backref="order", lazy="selectin")

    @hybrid_property
    def total_sum(self):
        return sum(product.quantity * product.price for product in self.products)


    @total_sum.expression
    def total_sum(cls):
        return (
            select(
                func.sum(OrderProduct.quantity * OrderProduct.price).where(OrderProduct.order_id == cls.id).scolar_subquery()
            )
        )


class OrderProduct(Base, IntIdMixin):
    __tablename__ = 'order_products'

    order_id = Column(BigInteger, ForeignKey('orders.id', ondelete="CASCADE"), nullable=True)
    product_id = Column(BigInteger, ForeignKey('products.id'), nullable=False)
    quantity = Column(BigInteger, nullable=False, default=1)
    price = Column(Numeric(20, 2), nullable=False)

    __table_args__ = (
        UniqueConstraint('order_id', 'product_id', name='order_product_id'),
    )
