from fastapi import APIRouter, Depends
from fastapi_utils.cbv import cbv

from app.product.dependencies import get_characteristics_manager, get_product_or_404, get_characteristics_or_404
from app.product.managers.characteristics_manager import ProductCharacteristicsManager
from app.product.models import Product, ProductCharacteristics
from app.product.schemas import ProductCharacteristicsCreate, ProductCharacteristicsUpdate

router = APIRouter(
    prefix="{product_id}/characteristics",
    tags=["characteristics"]
)

@cbv(router)
class CharacteristicsRouter:
    manager: ProductCharacteristicsManager = Depends(get_characteristics_manager)


    @router.post("/")
    async def create(
            self,
            request: ProductCharacteristicsCreate,
            product: Product = Depends(get_product_or_404),
    ):
        await self.manager.create_characteristic(request, product)


    @router.get("/")
    async def list(
            self,
            product: Product = Depends(get_product_or_404),
    ):
        characteristics = await self.manager.get_all(product)
        return characteristics


    @router.get("/{characteristic_id}")
    async def detail(
            self,
            characteristics: ProductCharacteristics = Depends(get_characteristics_or_404)
    ):
        return characteristics


    @router.put("/{characteristic_id}")
    async def update(
            self,
            request: ProductCharacteristicsUpdate,
            characteristics: ProductCharacteristics = Depends(get_characteristics_or_404)
    ):
        await self.manager.update_characteristic(request, characteristics)


    @router.post("/{characteristic_id}")
    async def delete(
            self,
            characteristics: ProductCharacteristics = Depends(get_characteristics_or_404)
    ):
        await self.manager.delete_characteristic(characteristics)


