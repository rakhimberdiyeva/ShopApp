from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from app.auth.dependencies import is_admin
from app.product.dependencies import get_characteristics_manager, get_product_or_404, get_characteristics_or_404
from app.product.managers.characteristics_manager import ProductCharacteristicsManager
from app.product.models import Product, ProductCharacteristics
from app.product.schemas import ProductCharacteristicsCreate, ProductCharacteristicsUpdate

router = APIRouter(
    prefix="/{product_id}/characteristics",
    tags=["characteristics"]
)

@cbv(router)
class CharacteristicsRouter:
    manager: ProductCharacteristicsManager = Depends(get_characteristics_manager)


    @router.post(
        "/",
        summary="создание характеристики",
        dependencies=[
            Depends(is_admin)
        ]
    )
    async def create(
            self,
            request: ProductCharacteristicsCreate,
            product: Product = Depends(get_product_or_404),
    ):
        """
        Эндпоинт для создания характеристики
        """
        await self.manager.create_characteristic(request, product)


    @router.get(
        "/",
        summary="получение всех характеристик",
    )
    async def list(
            self,
            product: Product = Depends(get_product_or_404),
    ):
        """
        Эндпоинт для получения всех характеристик
        """
        characteristics = await self.manager.get_all(product)
        return characteristics


    @router.get(
        "/{characteristic_id}",
        summary="получение характеристики",
    )
    async def detail(
            self,
            characteristics: ProductCharacteristics = Depends(get_characteristics_or_404)
    ):
        """
        Эндпоинт для получения характеристики
        """
        return characteristics


    @router.put(
        "/{characteristic_id}",
        summary="обновление характеристики",
        dependencies=[
            Depends(is_admin)
        ]
    )
    async def update(
            self,
            request: ProductCharacteristicsUpdate,
            characteristics: ProductCharacteristics = Depends(get_characteristics_or_404),
    ):
        """
        Эндпоинт для обновления характеристики
        """
        await self.manager.update_characteristic(request, characteristics)


    @router.delete(
        "/{characteristic_id}",
        summary="удаление характеристики",
        dependencies=[
            Depends(is_admin)
        ]
    )
    async def delete(
            self,
            characteristics: ProductCharacteristics = Depends(get_characteristics_or_404),
    ):
        """
        Эндпоинт для удаления характеристики
        """
        await self.manager.delete_characteristic(characteristics)


