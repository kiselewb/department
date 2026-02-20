from sqlalchemy.ext.asyncio import AsyncSession

from app.models.department import Department
from app.repositories.base import BaseRepository


class DepartmentRepository(BaseRepository[Department]):
    def __init__(self, session: AsyncSession):
        super().__init__(Department, session)
