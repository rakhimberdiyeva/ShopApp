from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.product.models import ProductImages


class ProductImageRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            product_id: int,
            filename,
            file_path
    ):
        """
        Функция для создания изображения продукта

        :param product_id: ИД продукта
        :param filename: название файла
        :param file_path: путь файла

        :return: ничего
        """

        image = ProductImages(
            product_id=product_id,
            filename=filename,
            file_path=file_path,

        )
        self.session.add(image)
        await self.session.flush()


    async def delete(
            self,
            image: ProductImages,
    ):
        """
        Функция для удаления изображения продукта

        :param image: моделька изображения

        :return: ничего
        """
        await self.session.delete(image)
        await self.session.flush()

    async def get_by_filename(
            self,
            filename: str,
    ):
        """
        Функция для получения изображения продукта по названию

        :param filename: название файла

        :return: моделька изображения
        """
        stmt = select(ProductImages).where(ProductImages.filename == filename)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()
