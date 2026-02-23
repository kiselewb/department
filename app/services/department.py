from collections import defaultdict
from app.repositories.department import DepartmentRepository
from app.schemas import DepartmentCreate, DepartmentUpdate
from app.schemas.department import DepartmentDeleteMode
from app.utils.exceptions import (
    RequestBodyRequiredException,
    DepartmentNotFoundException,
    ParentDepartmentNotFoundException,
    DepartmentCycleException,
    DepartmentNotSelfParentException,
    ReassignModeException,
    TargetDepartmentNotFoundException,
    ReassignToSelfException,
)


class DepartmentService:
    def __init__(self, repository: DepartmentRepository):
        self.repository = repository

    async def get_departments(self):
        return await self.repository.get_all()

    async def get_department_by_id(
        self, department_id: int, depth: int, include_employees: bool
    ):
        rows = await self.repository.get_department_tree(department_id, depth)

        if not rows:
            raise DepartmentNotFoundException()

        if include_employees:
            department_ids = [row["id"] for row in rows]
            employees = await self.repository.get_employees_by_departments(
                department_ids
            )

            employees_tree = defaultdict(list)
            for emp in employees:
                employees_tree[emp.department_id].append(emp)

            return self._build_tree(rows, employees_tree)
        else:
            return self._build_tree(rows)

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

    async def delete_department(
        self, department_id: int, mode: str, reassign_to_department_id: int | None
    ):
        if not await self.repository.get_one_or_none(id=department_id):
            raise DepartmentNotFoundException()

        if mode == DepartmentDeleteMode.reassign and reassign_to_department_id is None:
            raise ReassignModeException()

        if mode == DepartmentDeleteMode.reassign:
            if reassign_to_department_id == department_id:
                raise ReassignToSelfException()

            if not await self.repository.get_one_or_none(id=reassign_to_department_id):
                raise TargetDepartmentNotFoundException()

            await self.repository.delete_department_reassign(
                department_id, reassign_to_department_id
            )
        else:
            await self.repository.delete_department_cascade(department_id)

    def _build_tree(
        self, rows: list, employees_tree: dict | None = None
    ) -> dict | None:
        nodes = {}
        root = None

        for row in rows:
            node = {
                "id": row["id"],
                "name": row["name"],
                "parent_id": row["parent_id"],
                "created_at": row["created_at"],
                "employees": employees_tree.get(row["id"], [])
                if employees_tree
                else [],
                "children": [],
            }
            nodes[row["id"]] = node

            if row["depth"] == 0:
                root = node

        for row in rows:
            if row["depth"] > 0:
                parent = nodes.get(row["parent_id"])
                if parent:
                    parent["children"].append(nodes[row["id"]])

        return root
