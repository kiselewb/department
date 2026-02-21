from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class EmployeeBase(BaseModel):
    full_name: str = Field(min_length=1, max_length=200)
    position: str = Field(min_length=1, max_length=200)
    hired_at: date | None = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("full_name", "position", mode="before")
    @classmethod
    def strip_and_validate(cls, v: str) -> str:
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("Полное имя и позиция не должны быть пустыми")
        return v


class EmployeeCreate(EmployeeBase):
    department_id: int


class EmployeeRead(EmployeeCreate):
    id: int
    created_at: datetime
