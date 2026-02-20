from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class DepartmentBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    parent_id: int | None = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, v: str) -> str:
        if isinstance(v, str):
            v = v.strip()
        return v


class DepartmentCreate(DepartmentBase):
    pass


class DepartmentUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    parent_id: int | None = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator("name", mode="before")
    @classmethod
    def strip_name(cls, v: str | None) -> str | None:
        if isinstance(v, str):
            v = v.strip()
            if not v:
                raise ValueError("Название подразделения должно содержать символы")
        return v


class DepartmentRead(DepartmentBase):
    id: int
    created_at: datetime


class DepartmentTree(DepartmentRead):
    employees: list["EmployeeRead"] = []
    children: list["DepartmentTree"] = []


from app.schemas.employee import EmployeeRead  # noqa: E402


DepartmentTree.model_rebuild()

