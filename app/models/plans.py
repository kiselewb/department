from sqlalchemy import String, Numeric
from decimal import Decimal
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Plans(Base):
    __tablename__ = "plans"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(100), nullable=False)
    duration_days: Mapped[int] = mapped_column(nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
