from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.order.models import Order, OrderProduct
from app.order.schemas import OrderProductsCreate
from app.product.dependencies import get_product_or_404


class OrderProductsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            products: list[OrderProductsCreate],
            order: Order
    ):
        order_products = [
            OrderProduct(
                order_id=order.id,
                quantity=product.quantity,
                price=product.price,
                product_id=product.product_id
            )
            for product in products
        ]

        self.session.add_all(order_products)
        await self.session.flush()


    async def get(
            self,
            order: Order,
            order_product: OrderProduct
    ):
        stmt = select(OrderProduct).where(OrderProduct.order_id == order.id, OrderProduct.product_id==order_product.product_id)
        result = await self.session.execute(stmt)
        products = result.scalar_one_or_none()
        return products


    async def get_all(
            self,
            order: Order
    ):
        stmt = select(OrderProduct).where(OrderProduct.order_id == order.id)
        result = await self.session.execute(stmt)
        products = result.scalars().all()
        return products


    async def delete(
            self,
            order: Order,
            order_product: OrderProduct
    ) -> None:
        stmt = delete(OrderProduct).where(OrderProduct.order_id == order.id, OrderProduct.product_id == order_product.product_id)
        await self.session.execute(stmt)
        await self.session.flush()