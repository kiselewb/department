from app.repositories.department import DepartmentRepository
from app.schemas import DepartmentCreate, DepartmentUpdate
from app.utils.exceptions import (
    RequestBodyRequiredException,
    DepartmentNotFoundException,
    ParentDepartmentNotFoundException,
    DepartmentCycleException,
    DepartmentNotSelfParentException,
)


class DepartmentService:
    def __init__(self, repository: DepartmentRepository):
        self.repository = repository

    async def get_departments(self, *filter, **filter_by):
        return await self.repository.get_all(*filter, **filter_by)

    async def create_department(self, department_data: DepartmentCreate):
        return await self.repository.create_department(department_data)

    async def update_department(self, department_id: int, data: DepartmentUpdate):
        new_department_data = data.model_dump(exclude_unset=True)

        if not new_department_data:
            raise RequestBodyRequiredException()

        department = await self.repository.get_one_or_none(id=department_id)

        if not department:
            raise DepartmentNotFoundException()

        if "parent_id" in new_department_data:
            new_parent_id = new_department_data.get("parent_id")

            if new_parent_id is not None:
                if new_parent_id == department_id:
                    raise DepartmentNotSelfParentException()

                new_parent = await self.repository.get_one_or_none(id=new_parent_id)
                if not new_parent:
                    raise ParentDepartmentNotFoundException()

                if await self.repository.is_department_descendant(
                    department_id, new_parent_id
                ):
                    raise DepartmentCycleException()

        return await self.repository.update_department(
            department_id, new_department_data
        )
