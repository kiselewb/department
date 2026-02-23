from asyncpg.exceptions import ForeignKeyViolationError
from loguru import logger
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee import Employee
from app.repositories.base import BaseRepository
from app.schemas.employee import EmployeeBase, EmployeeCreate
from app.utils.exceptions import DepartmentNotFoundException


class EmployeeRepository(BaseRepository[Employee]):
    def __init__(self, session: AsyncSession):
        super().__init__(Employee, session)

    async def create_employee(self, department_id: int, data: EmployeeBase):
        employee_data = EmployeeCreate(**data.model_dump(), department_id=department_id)

        try:
            return await self.create(employee_data)

        except IntegrityError as e:
            await self.session.rollback()
            logger.warning(
                f"Ошибка в создании работника: {e.orig.__cause__.__class__.__name__}"
            )
            if isinstance(e.orig.__cause__, ForeignKeyViolationError):
                raise DepartmentNotFoundException()
            else:
                raise
