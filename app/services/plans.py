from app.repositories.plans import PlansRepository
from app.schemas.plans import PlansCreate
from app.utils.exceptions import PlanNotFound


class PlansService:
    def __init__(self, repository: PlansRepository):
        self.repository = repository

    async def get_plans(self, *filter, **filter_by):
        return await self.repository.get_all(*filter, **filter_by)

    async def get_plan_by_id(self, plan_id: int):
        plan = await self.repository.get_one_or_none(id=plan_id)
        if not plan:
            raise PlanNotFound
        return plan

    async def create_plan(self, plan_data: PlansCreate):
        return await self.repository.create(plan_data)

    async def delete_plan_by_id(self, plan_id: int):
        return await self.repository.delete(id=plan_id)
