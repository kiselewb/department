from typing import Sequence

from fastapi import APIRouter

from app.api.dependencies import EmployeeServiceDependency
from app.schemas.employee import EmployeeRead


router = APIRouter(prefix="/employees", tags=["Employees"])


@router.get("/")
async def get_employees(service: EmployeeServiceDependency) -> Sequence[EmployeeRead]:
    return await service.get_employees()
