from app.repositories.department import DepartmentRepository


class DepartmentService:
    def __init__(self, repository: DepartmentRepository):
        self.repository = repository

    async def get_departments(self, *filter, **filter_by):
        return await self.repository.get_all(*filter, **filter_by)
