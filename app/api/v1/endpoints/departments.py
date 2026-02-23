from typing import Sequence

from fastapi import APIRouter, Query

from app.api.dependencies import DepartmentServiceDependency, EmployeeServiceDependency
from app.schemas import EmployeeRead, DepartmentTree
from app.schemas.department import (
    DepartmentRead,
    DepartmentCreate,
    DepartmentUpdate,
    DepartmentDeleteMode,
)
from app.schemas.employee import EmployeeBase

router = APIRouter(prefix="/departments", tags=["Departments"])


@router.get("/")
async def get_departments(
    service: DepartmentServiceDependency,
) -> Sequence[DepartmentRead]:
    return await service.get_departments()


@router.get("/{department_id}")
async def get_department(
    service: DepartmentServiceDependency,
    department_id: int,
    depth: int = Query(default=1, ge=1, le=5),
    include_employees: bool = Query(default=True),
) -> DepartmentTree:
    return await service.get_department_by_id(department_id, depth, include_employees)


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


@router.delete("/{department_id}", status_code=204)
async def delete_department(
    service: DepartmentServiceDependency,
    department_id: int,
    mode: DepartmentDeleteMode,
    reassign_to_department_id: int | None = Query(None, gt=0),
):
    await service.delete_department(department_id, mode, reassign_to_department_id)


@router.post("/{department_id}/employees/")
async def create_employee_in_department(
    service: EmployeeServiceDependency, department_id: int, employee_data: EmployeeBase
) -> EmployeeRead:
    return await service.create_employee(department_id, employee_data)
