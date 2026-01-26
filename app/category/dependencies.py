from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.category.manager import CategoryManager
from app.core.dependencies import get_db


async def get_category_manager(
    session: AsyncSession = Depends(get_db)
):
    """
    Функция для создания объекта CategoryManager
    :param session: сессия дб
    :return: объект CategoryManager
    """
    return CategoryManager(session)