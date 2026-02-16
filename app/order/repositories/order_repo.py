from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.order.models import Order



class OrderRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            user_id,
            address,
            phone_number,
            comment,
            status,
    ) -> Order:
        """
        Функция для создания заказа

        :param user_id: Ид пользователя
        :param address: адрес
        :param phone_number: номер телефона
        :param comment: комментарий
        :param status: статус


        :return: моделька заказа
        """

        stmt = insert(Order).values(
            user_id=user_id,
            address=address,
            phone_number=phone_number,
            comment=comment,
            status=status
        ).returning(Order)

        result = await self.session.execute(stmt)
        await self.session.flush()
        product = result.scalars().first()
        return product


    async def update(
            self,
            order: Order,
            user_id,
            address,
            phone_number,
            comment,
    ) -> None:
        """
        Функция для обновления заказа

        :param order: моделька заказа
        :param user_id: Ид пользователя
        :param address: адрес
        :param phone_number: номер телефона
        :param comment: комментарий

        :return: ничего
        """

        order.user_id = user_id
        order.address = address
        order.phone_number = phone_number
        order.comment = comment
        self.session.add(order)
        await self.session.flush()


    async def update_status(
            self,
            order: Order,
            status
    ) -> None:
        """
        Функция для обновления статуса заказа

        :param order: моделька заказа
        :param status: статус

        :return: ничего
        """

        order.status = status
        self.session.add(order)
        await self.session.flush()



    async def delete(
            self,
            order: Order,
    ) -> None:
        """
        Функция для удаления заказа

        :param order: моделька заказа

        :return: ничего
        """

        await self.session.delete(order)
        await self.session.flush()


    async def get_by_id(
            self,
            order_id: int
    ) -> Order:
        """
        Функция для получения заказа по ИД

        :param order_id: Ид заказа

        :return: моделька заказа
        """

        stmt = select(Order).where(Order.id == order_id)
        result = await self.session.execute(stmt)
        order = result.scalar_one_or_none()
        return order


    async def get_all(
            self,
    ):
        """
        Функция для получения всех заказов

        :return: список заказов
        """
        stmt = select(Order)
        result = await self.session.execute(stmt)
        return result.scalars().all()
