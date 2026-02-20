from pydantic import BaseModel, ConfigDict, Field
from decimal import Decimal


class PlansBase(BaseModel):
    title: str
    duration_days: int = Field(gt=0)
    price: Decimal = Field(
        gt=0, max_digits=10, decimal_places=2, examples=[Decimal("9.99")]
    )

    model_config = ConfigDict(from_attributes=True)


class PlansCreate(PlansBase):
    pass


class PlansRead(PlansBase):
    id: int
