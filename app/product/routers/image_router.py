from fastapi import APIRouter, Depends, UploadFile, File
from fastapi_utils.cbv import cbv
from fastapi.responses import FileResponse

from app.auth.dependencies import is_admin
from app.product.dependencies import get_product_or_404, get_product_images_manager, get_product_images_or_404
from app.product.managers.image_manager import ProductImageManager
from app.product.models import Product, ProductImages

router = APIRouter(
    prefix="/{product_id}/images",
    tags=["images"]

)

@cbv(router)
class ImageRouter:
    manager: ProductImageManager = Depends(get_product_images_manager)
    product: Product = Depends(get_product_or_404)

    @router.post(
        "/",
        summary="создание изображения продукта",
        dependencies=[
            Depends(is_admin)
        ]
    )
    async def upload(
            self,
            file: UploadFile = File(...)
    ):
        """
        Эндпоинт для загрузки изображения продукта
        """
        await self.manager.create(product=self.product, file=file)


    @router.get(
        "/{filename}",
        summary="получение изображения продукта",
        dependencies=[
            Depends(is_admin)
        ]
    )
    async def get_by_filename(
            self,
            image: ProductImages = Depends(get_product_images_or_404),
    ):
        """
        Эндпоинт для получения изображения продукта по имени файла
        """
        return FileResponse(image.file_path)


    @router.delete(
        "/{filename}",
        summary="удаление изображения продукта",
        dependencies=[
            Depends(is_admin)
        ]
    )
    async def delete(
            self,
            image: ProductImages = Depends(get_product_images_or_404)
    ):
        """
        Эндпоинт для удаления изображения продукта
        """
        await self.manager.delete(image)