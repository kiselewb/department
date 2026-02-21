from typing import Sequence

from fastapi import APIRouter

from app.api.dependencies import DepartmentServiceDependency
from app.schemas.department import DepartmentRead, DepartmentCreate, DepartmentUpdate

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("/")
async def get_departments(
    service: DepartmentServiceDependency,
) -> Sequence[DepartmentRead]:
    return await service.get_departments()


@router.post("/")
async def create_department(
    service: DepartmentServiceDependency, department_data: DepartmentCreate
) -> DepartmentRead:
    return await service.create_department(department_data)


@router.patch("/{department_id}")
async def update_department(
    service: DepartmentServiceDependency,
    department_id: int,
    new_department_data: DepartmentUpdate,
) -> DepartmentRead:
    return await service.update_department(department_id, new_department_data)
