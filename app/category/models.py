from sqlalchemy import Column, String

from app.core.models import Base, IntIdMixin, TimeActionMixin


class Category(Base, IntIdMixin, TimeActionMixin):
     __tablename__ = 'categories'

     name = Column(String(512), nullable=False)
     description = Column(String(1024), nullable=True)
