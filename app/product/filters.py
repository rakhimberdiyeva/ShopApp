from fastapi_filter.contrib.sqlalchemy import Filter

from app.product.models import Product


class ProductFilter(Filter):
    q: str | None = None
    category_id: int | None  = None
    order_by: list[str] | None  = None

    class Constants(Filter.Constants):
        model = Product
        search_model_fields = ("name", )
        search_field_name = "q"