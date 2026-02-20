from sqlalchemy.ext.asyncio import AsyncSession

from app.models.plans import Plans
from app.repositories.base import BaseRepository


class PlansRepository(BaseRepository[Plans]):
    def __init__(self, session: AsyncSession):
        super().__init__(Plans, session)
