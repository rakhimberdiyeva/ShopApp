from sqlalchemy import select, Insert, insert, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.category.models import Category


class CategoryRepository:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session


    async def create_category(
            self,
            name: str,
            description: str,
    ) -> Category:
        stmt = insert(Category).values(
            name=name,
            description=description,
        ).returning(Category)
        result = await self.session.execute(stmt)
        await self.session.flush()
        category = result.scalars().first()
        return category


    async def get_category_by_id(
            self,
            category_id: int
    ) -> Category | None:
        stmt = select(Category).where(Category.id == category_id)
        result = await self.session.execute(stmt)
        category = result.scalar_one_or_none()
        return category


    async def get_categories(
            self,
    ):
        stmt = select(Category)
        result = await self.session.execute(stmt)
        categories = result.scalars().all()
        return categories


    async def update_category(
            self,
            category_id: int,
            name: str,
            description: str,
    ) -> None:
        stmt = update(Category).where(Category.id == category_id).values(
            name=name,
            description=description,
        )
        result = await self.session.execute(stmt)
        await self.session.flush()



    async def delete_category(
            self,
            category_id: int
    ) -> None:
        stmt = delete(Category).where(Category.id == category_id)
        await self.session.execute(stmt)
        await self.session.flush()