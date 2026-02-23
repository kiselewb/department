from app.models import Department
from app.repositories.department import DepartmentRepository
from app.schemas import DepartmentCreate, DepartmentUpdate
from app.schemas.department import DepartmentDeleteMode
from app.utils.exceptions import (
    RequestBodyRequiredException,
    DepartmentNotFoundException,
    ParentDepartmentNotFoundException,
    DepartmentCycleException,
    DepartmentNotSelfParentException, ReassignModeException, TargetDepartmentNotFoundException, ReassignToSelfException,
)


class DepartmentService:
    def __init__(self, repository: DepartmentRepository):
        self.repository = repository

    async def get_departments(self):
        return await self.repository.get_all()

    async def get_department_by_id(self, department_id: int) -> Department:
        pass

    async def create_department(self, data: DepartmentCreate):
        return await self.repository.create_department(data)

    async def update_department(self, department_id: int, data: DepartmentUpdate):
        new_department_data = data.model_dump(exclude_unset=True)

        if not new_department_data:
            raise RequestBodyRequiredException()

        if not await self.repository.get_one_or_none(id=department_id):
            raise DepartmentNotFoundException()

        if "parent_id" in new_department_data:
            new_parent_id = new_department_data.get("parent_id")

            if new_parent_id is not None:
                if new_parent_id == department_id:
                    raise DepartmentNotSelfParentException()

                if not await self.repository.get_one_or_none(id=new_parent_id):
                    raise ParentDepartmentNotFoundException()

                if await self.repository.is_department_descendant(
                    department_id, new_parent_id
                ):
                    raise DepartmentCycleException()

        return await self.repository.update_department(
            department_id, new_department_data
        )

    async def delete_department(self, department_id: int, mode: str, reassign_to_department_id: int | None):
        if not await self.repository.get_one_or_none(id=department_id):
            raise DepartmentNotFoundException()

        if mode == DepartmentDeleteMode.reassign and reassign_to_department_id is None:
            raise ReassignModeException()

        if mode == DepartmentDeleteMode.reassign:
            if reassign_to_department_id == department_id:
                raise ReassignToSelfException()

            if not await self.repository.get_one_or_none(id=reassign_to_department_id):
                raise TargetDepartmentNotFoundException()

            await self.repository.delete_department_reassign(department_id, reassign_to_department_id)
        else:
            await self.repository.delete_department_cascade(department_id)