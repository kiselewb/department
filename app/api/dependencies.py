from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.session import get_session_db
from app.repositories.plans import PlansRepository
from app.services.plans import PlansService


def get_plans_service(session: AsyncSession = Depends(get_session_db)) -> PlansService:
    return PlansService(PlansRepository(session))


PlansServiceDependency = Annotated[PlansService, Depends(get_plans_service)]
