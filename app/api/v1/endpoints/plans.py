from typing import Sequence

from fastapi import APIRouter, Body

from app.api.dependencies import PlansServiceDependency
from app.api.exceptions import PlanNotFoundHTTPException
from app.schemas.plans import PlansRead, PlansCreate
from app.utils.exceptions import PlanNotFound

router = APIRouter(prefix="/plans", tags=["Plans"])


@router.get("/")
async def get_plans(service: PlansServiceDependency) -> Sequence[PlansRead]:
    return await service.get_plans()


@router.get("/{plan_id}")
async def get_plan(service: PlansServiceDependency, plan_id: int) -> PlansRead | None:
    try:
        return await service.get_plan_by_id(plan_id)
    except PlanNotFound:
        raise PlanNotFoundHTTPException


@router.post("/")
async def create_plan(
    service: PlansServiceDependency,
    plan_data: PlansCreate = Body(),
) -> dict[str, str | PlansRead]:
    new_plan = await service.create_plan(plan_data)
    return {"status": "OK", "new_plan": new_plan}


@router.delete("/{plan_id}")
async def delete_plan(
    service: PlansServiceDependency, plan_id: int
) -> dict[str, str | PlansRead]:
    deleted_plan = await service.delete_plan_by_id(plan_id)
    return {"status": "OK", "deleted_plan": deleted_plan}
