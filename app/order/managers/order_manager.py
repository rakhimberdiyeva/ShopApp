from typing import List

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.core.exceptions import NotFound
from app.order.models import Order
from app.order.repositories.order_product_repo import OrderProductsRepository
from app.order.repositories.order_repo import OrderRepository
from app.order.schemas import OrderCreate, OrderUpdate, OrderStatusUpdate


class OrderManager:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session
        self.order_repo = OrderRepository(self.session)
        self.order_product_repo = OrderProductsRepository(self.session)

    async def create(
            self,
            request: OrderCreate,
            user: User
    ) -> Order:
        order = await self.order_repo.create(
            user_id=user.id,
            **request.model_dump(exclude={"products"})
        )
        await self.order_product_repo.create(
            request.products,
            order=order,
        )
        await self.session.commit()
        await self.session.refresh(order)
        return order


    async def get_by_id(self, order_id: int) -> Order:
        order = await self.order_repo.get_by_id(order_id)
        if not order:
            raise NotFound(f"Order with id {order_id} not found")
        return order


    async def get_all(self, filters) -> list[Order]:
        orders = await self.order_repo.get_all(filters)
        return orders


    async def delete(self, order: Order) -> None:
        await self.order_repo.delete(order)
        await self.session.commit()


    async def update(
            self,
            request: OrderUpdate,
            order: Order
    ):
        await self.order_repo.update(
            order,
            **request.model_dump(exclude={"products"})
        )
        await self.order_product_repo.clear(order.id)
        await self.order_product_repo.create(
            request.products,
            order=order
        )
        await self.session.commit()


    async def update_status(
            self,
            request: OrderStatusUpdate,
            order: Order
    ):
        await self.order_repo.update_status(order, request.status)
        await self.session.commit()