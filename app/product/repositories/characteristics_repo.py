from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.product.models import ProductCharacteristics


class ProductCharacteristicsRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            name,
            value,
            product_id,
    ) -> ProductCharacteristics:
        """
        Функция для создания продукта

        :param name: название продукта
        :param short_description: краткое описание продукта
        :param long_description: длинное описание продукта
        :param price: цена продукта
        :param category_id: Ид категории продукта


        :return: моделька продукта
        """

        stmt = insert(ProductCharacteristics).values(
            name=name,
            value=value,
            product_id=product_id,
        ).returning(ProductCharacteristics)

        result = await self.session.execute(stmt)
        await self.session.flush()
        characteristics = result.scalars().first()
        return characteristics



    async def update(
            self,
            characteristic_id: int,
            name,
            value,
            product_id,
    ) -> None:
        """
        Функция для обновления продукта

        :param product_id: нИд продукта
        :param name: название продукта
        :param short_description: краткое описание продукта
        :param long_description: длинное описание продукта
        :param price: цена продукта
        :param category_id: Ид категории продукта


        :return: ничего
        """

        stmt = update(ProductCharacteristics).where(ProductCharacteristics.id == characteristic_id).values(
            name=name,
            value=value,
            product_id=product_id,
        )
        await self.session.execute(stmt)
        await self.session.flush()



    async def delete(
            self,
            characteristic_id
    ) -> None:
        """
        Функция для удаления продукта

        :param product_id: нИд продукта

        :return: ничего
        """

        stmt = delete(ProductCharacteristics).where(ProductCharacteristics.id == characteristic_id)
        await self.session.execute(stmt)
        await self.session.flush()


    async def get_by_id(
            self,
            characteristic_id
    ) -> ProductCharacteristics:
        """
        Функция для получения продукта по ИД

        :param product_id: нИд продукта

        :return: моделька продукта
        """

        stmt = select(ProductCharacteristics).where(ProductCharacteristics.id == characteristic_id)
        result = await self.session.execute(stmt)
        characteristics = result.scalar_one_or_none()
        return characteristics

    async def get_all(self):
        pass
