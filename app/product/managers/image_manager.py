import shutil
import uuid

from fastapi import UploadFile

from app.core.settings import BASE_DIR
from app.product.models import Product, ProductImages
from app.product.repositories.image_repo import ProductImageRepository
from app.product.repositories.product_repo import ProductRepository


class ProductImageManager:
    def __init__(self, session):
        self.session = session
        self.repo = ProductImageRepository(session)
        self.product_repo = ProductRepository(session)


    async def create(
            self,
            product: Product,
            file: UploadFile
    ):
        """
        Метод для создания изображения продукта

        :param product: объект продукта
        :param file: загружаемый файл
        :return: объект изображения
        """
        filename = f"{uuid.uuid4()}.{file.filename}"
        filepath = BASE_DIR / "uploads" / filename

        with open(filepath, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        await self.repo.create(product_id=product.id, filename=filename, file_path=str(filepath))
        await self.session.commit()


    async def delete(
            self,
            product_image: ProductImages
    ):
        """
        Метод для удаления изображения продукта

        :param product_image: объект изображения
        :return: ничего
        """
        await self.session.delete(product_image)
        await self.session.commit()


    async def get_by_filename(self, filename: str):
        """
        Метод для получения изображения продукта по имени файла

        :param filename: имя файла
        :return: объект изображения
        """
        image = await self.repo.get_by_filename(filename)
        if not image:
            raise FileNotFoundError
        return image