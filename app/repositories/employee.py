from sqlalchemy.ext.asyncio import AsyncSession

from app.models.employee import Employee
from app.repositories.base import BaseRepository


class EmployeeRepository(BaseRepository[Employee]):
    def __init__(self, session: AsyncSession):
        super().__init__(Employee, session)
