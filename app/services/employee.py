from app.repositories.employee import EmployeeRepository


class EmployeeService:
    def __init__(self, repository: EmployeeRepository):
        self.repository = repository

    async def get_employees(self, *filter, **filter_by):
        return await self.repository.get_all(*filter, **filter_by)
