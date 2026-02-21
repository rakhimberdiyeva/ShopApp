from app.product.routers.product_router import router as product_router
from app.product.routers.characteristics_router import router as characteristics_router
from app.product.routers.review_router import router as review_router
from app.product.routers.image_router import router as image_router

product_router.include_router(characteristics_router)
product_router.include_router(review_router)
product_router.include_router(image_router)