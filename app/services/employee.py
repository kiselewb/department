from loguru import logger

from app.repositories.employee import EmployeeRepository
from app.schemas.employee import EmployeeBase


class EmployeeService:
    def __init__(self, repository: EmployeeRepository):
        self.repository = repository

    async def get_employees(self, *filter, **filter_by):
        return await self.repository.get_all(*filter, **filter_by)

    async def create_employee(self, department_id: int, data: EmployeeBase):
        logger.info(
            f"Создание работника в подразделении(id={department_id}), data={data.model_dump()}"
        )
        result = await self.repository.create_employee(department_id, data)
        logger.info(f"Работник успешно создан: {result!r}")
        return result
