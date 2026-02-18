from fastapi_filter.contrib.sqlalchemy import Filter

from app.order.models import Order


class OrderFilter(Filter):
    user_id: int | None = None
    status: str | None  = None
    order_by: list[str] | None  = None

    class Constants(Filter.Constants):
        model = Order
        search_model_fields = ("user_id", "status")
        search_field_name = "q"