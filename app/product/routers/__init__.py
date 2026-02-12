from app.product.routers.product_router import router as product_router
from app.product.routers.characteristics_router import router as characteristics_router

product_router.include_router(characteristics_router)