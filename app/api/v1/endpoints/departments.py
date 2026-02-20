from typing import Sequence

from fastapi import APIRouter

from app.api.dependencies import DepartmentServiceDependency
from app.schemas.department import DepartmentRead


router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("/")
async def get_departments(service: DepartmentServiceDependency) -> Sequence[DepartmentRead]:
    return await service.get_departments()
