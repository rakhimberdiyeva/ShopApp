from sqlalchemy.ext.asyncio import AsyncSession


from app.product.exceptions import CharacteristicNotFound
from app.product.models import ProductCharacteristics, Product
from app.product.repositories.characteristics_repo import ProductCharacteristicsRepository
from app.product.schemas import ProductCharacteristicsCreate, ProductCharacteristicsUpdate


class ProductCharacteristicsManager:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session
        self.characteristics_repo = ProductCharacteristicsRepository(session)


    async def create_characteristic(
            self,
            request: ProductCharacteristicsCreate,
            product: Product
    ) -> ProductCharacteristics:
        """
        Метод для создания характеристики продукта

        :param request: запрос с данными для создания
        :param product: моделька продукта

        :return: созданный продукт
        """
        characteristic = await self.characteristics_repo.create(
            **request.model_dump(),
            product_id=product.id
        )
        await self.session.commit()
        return characteristic


    async def get_characteristic(
            self,
            product: Product,
            characteristic_id: int
    ) -> ProductCharacteristics:
        """
        Метод для получения характеристики продукта по ИД

        :param product: моделька продукта
        :param characteristic_id: ИД характеристики

        :return: моделька характеристики
        """
        characteristic = await self.characteristics_repo.get_by_id(characteristic_id, product.id)
        if not characteristic:
            raise CharacteristicNotFound(
                "Характеристика продукта не найдена"
            )
        return characteristic



    async def get_all(
            self,
            product: Product,
    ):
        """
        Метод для получения всех характеристик продукта

        :param product: моделька продукта

        :return: список характеристик
        """
        characteristics = await self.characteristics_repo.get_all(product.id)
        return characteristics



    async def update_characteristic(
            self,
            request: ProductCharacteristicsUpdate,
            characteristic: ProductCharacteristics
    ) -> None:
        """
        Метод для обновления характеристики продукта

        :param request: запрос с данными для обновления
        :param characteristic: моделька характеристики

        :return: ничего
        """

        await self.characteristics_repo.update(
            characteristic,
            **request.model_dump(),
        )
        await self.session.commit()



    async def delete_characteristic(
            self,
            characteristic: ProductCharacteristics,
    ) -> None:
        """
        Метод для удаления характеристики продукта

        :param characteristic: моделька характеристики

        :return: ничего
        """

        await self.characteristics_repo.delete(
            characteristic
        )
        await self.session.commit()
