from sqlalchemy.ext.asyncio import AsyncSession

from app.product.dependencies import get_product_or_404
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
            product_id: int
    ) -> ProductCharacteristics:
        """
        Метод для создания характеристики продукта

        :param request: запрос с данными для создания
        :param product_id: ИД продукта

        :return: созданный продукт
        """
        await get_product_or_404(product_id, self.session)
        characteristic = await self.characteristics_repo.create(
            **request.model_dump(),
            product_id=product_id
        )
        await self.session.commit()
        return characteristic


    async def get_characteristic(
            self,
            characteristic_id: int
    ) -> ProductCharacteristics:
        """
        Метод для получения характеристики продукта по ИД

        :param characteristic_id: ИД характеристики

        :return: моделька характеристики
        """
        characteristic = await self.characteristics_repo.get_by_id(characteristic_id)
        if not characteristic:
            raise CharacteristicNotFound(
                "Характеристика продукт не найдена"
            )
        return characteristic


    # TODO
    async def get_all(self):
        pass


    async def update_characteristic(
            self,
            request: ProductCharacteristicsUpdate,
            characteristic_id: int,
            product: Product
    ) -> None:
        """
        Метод для обновления характеристики продукта

        :param request: запрос с данными для обновления
        :param characteristic_id: ИД характеристики
        :param product: моделька продукта

        :return: ничего
        """

        await self.characteristics_repo.update(
            **request.model_dump(),
            characteristic_id=characteristic_id,
            product_id=product.id
        )
        await self.session.commit()



    async def delete_characteristic(
            self,
            characteristic_id: int
    ) -> None:
        """
        Метод для удаления характеристики продукта

        :param characteristic_id: ИД характеристики

        :return: ничего
        """

        await self.characteristics_repo.delete(
            characteristic_id=characteristic_id
        )
        await self.session.commit()
