from sqlalchemy import insert, update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.product.models import ProductReview


class ProductReviewRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(
            self,
            user_id,
            product_id,
            message,
            grade
    ) -> ProductReview:
        """
        Функция для создания отзыва продукта

        :param user_id: ИД пользователя
        :param product_id: ИД продукта
        :param message: текст
        :param grade: оценка

        :return: моделька отзыва
        """

        stmt = insert(ProductReview).values(
            user_id=user_id,
            product_id=product_id,
            message=message,
            grade=grade
        ).returning(ProductReview)

        result = await self.session.execute(stmt)
        await self.session.flush()
        review = result.scalars().first()
        return review


    async def update(
            self,
            review_id,
            user_id,
            product_id,
            message,
            grade
    ) -> None:
        """
        Функция для обновления отзыва продукта

        :param review_id: ИД отзыва
        :param user_id: ИД пользователя
        :param product_id: ИД продукта
        :param message: текст
        :param grade: оценка


        :return: ничего
        """

        stmt = update(ProductReview).where(ProductReview.id == review_id).values(
            user_id=user_id,
            product_id=product_id,
            message=message,
            grade=grade
        )
        await self.session.execute(stmt)
        await self.session.flush()


    async def delete(
            self,
            review_id
    ) -> None:
        """
        Функция для удаления отзыва продукта

        :param review_id: ИД отзыва

        :return: ничего
        """

        stmt = delete(ProductReview).where(ProductReview.id == review_id)
        await self.session.execute(stmt)
        await self.session.flush()


    async def get_by_id(
            self,
            review_id
    ) -> ProductReview:
        """
        Функция для получения продукта по ИД

        :param review_id: Ид отзыва

        :return: моделька отзыва
        """

        stmt = select(ProductReview).where(ProductReview.id == review_id)
        result = await self.session.execute(stmt)
        review = result.scalar_one_or_none()
        return review


    async def get_all(self):
        pass
