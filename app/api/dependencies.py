from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session_db
from app.repositories.department import DepartmentRepository
from app.services.department import DepartmentService
from app.repositories.employee import EmployeeRepository
from app.services.employee import EmployeeService


def get_department_service(session: AsyncSession = Depends(get_session_db)) -> DepartmentService:
    return DepartmentService(DepartmentRepository(session))

def get_employee_service(session: AsyncSession = Depends(get_session_db)) -> EmployeeService:
    return EmployeeService(EmployeeRepository(session))

DepartmentServiceDependency = Annotated[DepartmentService, Depends(get_department_service)]
EmployeeServiceDependency = Annotated[EmployeeService, Depends(get_employee_service)]
