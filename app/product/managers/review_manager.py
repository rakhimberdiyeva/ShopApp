from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.product.dependencies import get_product_or_404
from app.product.exceptions import ReviewNotFound
from app.product.models import ProductReview, Product
from app.product.repositories.review_repo import ProductReviewRepository
from app.product.schemas import ProductReviewCreate, ProductReviewUpdate


class ProductReviewManager:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session
        self.review_repo = ProductReviewRepository(session)


    async def create_review(
            self,
            request: ProductReviewCreate,
            user: User,
            product: Product
    ) -> ProductReview:
        """
        Метод для создания отзыва

        :param request: запрос с данными для создания
        :param user: моделька пользователя
        :param product: моделька продукта

        :return: созданный отзыв
        """

        review = await self.review_repo.create(
            **request.model_dump(),
            user_id=user.id,
            product_id=product.id
        )
        await self.session.commit()
        return review


    async def get_review(
            self,
            product: Product,
            review_id: int
    ) -> ProductReview:
        """
        Метод для получения отзыва по ИД

        :param product: моделька продукта
        :param review_id: ИД отзыва

        :return: моделька отзыва
        """
        review = await self.review_repo.get_by_id(review_id, product.id)
        if not review:
            raise ReviewNotFound(
                "Отзыв не найден"
            )
        return review


    async def get_all(
            self,
            product: Product,
    ):
        review = await self.review_repo.get_all(product.id)
        return review


    async def update_review(
            self,
            request: ProductReviewUpdate,
            review: ProductReview,
    ) -> None:
        """
        Метод для обновления отзыва

        :param request: запрос с данными для обновления
        :param review: моделька отзыва

        :return: ничего
        """

        await self.review_repo.update(
            review,
            **request.model_dump(),
        )
        await self.session.commit()



    async def delete_review(
            self,
            review: ProductReview
    ) -> None:
        """
        Метод для удаления отзыва

        :param review:: моделька отзыва

        :return: ничего
        """

        await self.review_repo.delete(
            review
        )
        await self.session.commit()
