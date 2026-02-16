from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.order.models import Order, OrderProduct


class OrderProductsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            order_id,
            product_id,
            quantity,
            price,
    ) -> Order:
        """
        Функция для создания продукта заказа

        :param order_id: Ид заказа
        :param product_id: Ид продукта
        :param quantity: количество
        :param price: цена

        :return: моделька продукта заказа
        """

        stmt = insert(Order).values(
            order_id=order_id,
            product_id=product_id,
            quantity=quantity,
            price=price,
        ).returning(Order)

        result = await self.session.execute(stmt)
        await self.session.flush()
        product = result.scalars().first()
        return product


    async def update(
            self,
            order_products: OrderProduct,
            order_id,
            product_id,
            quantity,
            price,
    ) -> None:
        """
        Функция для обновления продукта заказа

        :param order_products: моделька продукта заказа
        :param order_id: Ид заказа
        :param product_id: Ид продукта
        :param quantity: количество
        :param price: цена

        :return: ничего
        """

        order_products.order_id = order_id
        order_products.product_id = product_id
        order_products.quantity = quantity
        order_products.price = price
        self.session.add(order_products)
        await self.session.flush()



    async def delete(
            self,
            order_products: OrderProduct,
    ) -> None:
        """
        Функция для удаления продукта заказа

        :param order_products: моделька продукта заказа

        :return: ничего
        """

        await self.session.delete(order_products)
        await self.session.flush()


    async def get_by_id(
            self,
            order_product_id: int
    ) -> OrderProduct:
        """
        Функция для получения продуктов заказа по ИД

        :param order_product_id: моделька продуктов заказа

        :return: моделька продуктов заказов
        """

        stmt = select(Order).where(OrderProduct.id == order_product_id)
        result = await self.session.execute(stmt)
        order = result.scalar_one_or_none()
        return order


    async def get_all(
            self,
            order_id: int
    ):
        """
        Функция для получения всех продуктов заказа

        :param order_id: Ид заказа

        :return: список продуктов заказа
        """
        stmt = select(OrderProduct).where(OrderProduct.order_id == order_id)
        result = await self.session.execute(stmt)
        return result.scalars().all()
