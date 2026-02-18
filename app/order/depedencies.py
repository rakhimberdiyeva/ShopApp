from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.dependencies import get_db
from app.order.managers.order_manager import OrderManager


async def get_order_manager(
    session: AsyncSession = Depends(get_db)
):
    """
    Функция для создания объекта OrderManager

    :param session: сессия бд

    :return: объект OrderManager
    """

    return OrderManager(session)



async def get_order_or_404(
    order_id: int,
    manager: OrderManager = Depends(get_order_manager),
):
    """
    Функция для поиска заказа
    Если заказа нет вызывает ошибку 404

    :param order_id: ИД заказа
    :param manager: объект OrderManager

    :return: моделька заказа
    """

    return await manager.get_by_id(order_id)