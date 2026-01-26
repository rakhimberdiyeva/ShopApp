from sqlalchemy.ext.asyncio import AsyncSession

from app.category.models import Category
from app.category.repository import CategoryRepository
from app.category.schemas import CategoryCreate, CategoryRead, CategoryUpdate


class CategoryManager:
    def __init__(
            self,
            session: AsyncSession,
    ):
        self.session = session
        self.category_repo = CategoryRepository(session)


    async def create_category(
            self,
            request: CategoryCreate,
    ) -> Category:
        category = await self.category_repo.create_category(
            name=request.name,
            description=request.description,
        )
        await self.session.commit()
        return category


    async def get_category(
            self,
            category_id: int,
    ) -> Category | None:
        category = await self.category_repo.get_category_by_id(category_id)
        return category


    async def get_all_categories(
            self
    ) -> list[Category]:
        categories = await self.category_repo.get_categories()
        return categories


    async def update_category(
            self,
            category_id: int,
            request: CategoryUpdate,
    ) -> None:
        await self.category_repo.update_category(
            category_id=category_id,
            name=request.name,
            description=request.description,
        )
        await self.session.commit()


    async def delete_category(
            self,
            category_id: int
    ) -> None:
        await self.category_repo.delete_category(
            category_id=category_id
        )
        await self.session.commit()


