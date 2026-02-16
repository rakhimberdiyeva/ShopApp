from sqlalchemy.ext.asyncio import AsyncSession

from app.order.models import Order
from app.order.repositories.order_repo import OrderRepository
from app.order.schemas import OrderCreate


class OrderManager:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session
        self.order_repo = OrderRepository(session)

    async def create_order(
            self,
            request: OrderCreate,
    ) -> Order:
        order = await self.order_repo.create(
            **request.model_dump(),
        )
        await self.session.commit()
        return order




