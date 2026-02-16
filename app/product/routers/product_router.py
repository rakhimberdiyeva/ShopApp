from fastapi import APIRouter
from fastapi.params import Depends
from fastapi_filter import FilterDepends
from fastapi_utils.cbv import cbv

from app.auth.dependencies import is_admin
from app.product.dependencies import get_product_manager, get_product_or_404
from app.product.filters import ProductFilter
from app.product.managers.product_manager import ProductManager
from app.product.models import Product
from app.product.schemas import ProductUpdate, ProductCreate

router = APIRouter(
    prefix="/products",
    tags=["product"]
)

@cbv(router)
class ProductRouter:
    manager: ProductManager = Depends(get_product_manager)


    @router.post(
        "/",
        summary="создание продукта",
        dependencies=[
            Depends(is_admin)
        ]
    )
    async def create(
            self,
            request: ProductCreate,
    ):
        """
        Эндпоинт для создания продукта
        """
        await self.manager.create_product(request)


    @router.get(
        "/",
        summary="получение всех продуктов",
    )
    async def list(
            self,
            filters: ProductFilter = FilterDepends(ProductFilter),
    ):
        """
        Эндпоинт для получения всех продуктов
        """
        products = await self.manager.get_all(filters)
        return products


    @router.get(
        "/{product_id}",
        summary="получение продукта",
    )
    async def detail(
            self,
            product: Product = Depends(get_product_or_404)
    ):
        """
        Эндпоинт для получения продукта
        """
        return product


    @router.put(
        "/{product_id}",
        summary="обновление продукта",
        dependencies=[
            Depends(is_admin)
        ]
    )
    async def update(
            self,
            request: ProductUpdate,
            product: Product = Depends(get_product_or_404),
    ):
        """
        Эндпоинт для обновления продукта
        """
        await self.manager.update_product(request, product)


    @router.delete(
        "/{product_id}",
        summary="удаление продукта",
        dependencies=[
            Depends(is_admin)
        ]
    )
    async def delete(
            self,
            product: Product = Depends(get_product_or_404),
    ):
        """
        Эндпоинт для удаления продукта
        """
        await self.manager.delete_product(product)


