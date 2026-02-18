from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_filter import FilterDepends
from fastapi_utils.cbv import cbv

from app.auth.dependencies import get_current_user
from app.auth.models import User
from app.order.depedencies import get_order_or_404, get_order_manager
from app.order.filters import OrderFilter
from app.order.managers.order_manager import OrderManager
from app.order.models import Order
from app.order.schemas import OrderCreate

router = APIRouter(
    prefix="/order",
    tags=["order"]
)

@cbv(router)
class OrderRouter:
    manager: OrderManager = Depends(get_order_manager)


    @router.post(
        "/",
        summary="создание заказа",
    )
    async def create(
            self,
            request: OrderCreate,
            user: User = Depends(get_current_user)
    ):
        await self.manager.create(request, user)


    @router.get(
        "/",
        summary="получение всех заказов",
    )
    async def list(
            self,
            filters: OrderFilter = FilterDepends(OrderFilter),
    ):
        orders = await self.manager.get_all(filters)
        return orders


    @router.get(
        "/{order_id}",
        summary="получение заказа",
    )
    async def detail(
            self,
            order: Order = Depends(get_order_or_404)
    ):
        return order



    @router.delete(
        "/{order_id}",
        summary="удаление заказа",
    )
    async def delete(
            self,
            order: Order = Depends(get_order_or_404)
    ):

        await self.manager.delete(order)


