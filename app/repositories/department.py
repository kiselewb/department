from sqlalchemy import select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.exc import IntegrityError

from app.models import Employee
from app.models.department import Department
from app.repositories.base import BaseRepository
from app.schemas import DepartmentCreate, DepartmentUpdate
from asyncpg.exceptions import (
    ForeignKeyViolationError,
    CheckViolationError,
    UniqueViolationError,
)
from app.utils.exceptions import (
    ParentDepartmentNotFoundException,
    DepartmentNotSelfParentException,
    DepartmentNameExistsException,
)


class DepartmentRepository(BaseRepository[Department]):
    def __init__(self, session: AsyncSession):
        super().__init__(Department, session)

    async def create_department(self, data: DepartmentCreate):
        try:
            return await self.create(data)

        except IntegrityError as e:
            await self.session.rollback()
            if isinstance(e.orig.__cause__, ForeignKeyViolationError):
                raise ParentDepartmentNotFoundException()
            if isinstance(e.orig.__cause__, CheckViolationError):
                raise DepartmentNotSelfParentException()
            if isinstance(e.orig.__cause__, UniqueViolationError):
                raise DepartmentNameExistsException()
            else:
                raise

    async def is_department_descendant(
        self, department_id: int, new_parent_id: int
    ) -> bool:
        """
        WITH RECURSIVE subtree AS (
            SELECT id FROM departments WHERE id = :department_id
            UNION ALL
            SELECT d.id FROM departments d
            JOIN subtree s ON d.parent_id = s.id
        )
        SELECT EXISTS(SELECT id FROM subtree WHERE id = :new_parent_id)
        """
        subtree = (
            select(Department.id)
            .where(Department.id == department_id)
            .cte(name="subtree", recursive=True)
        )

        depart = aliased(Department)

        subtree = subtree.union_all(
            select(depart.id).join(subtree, depart.parent_id == subtree.c.id)
        )

        query = select(
            select(subtree.c.id)
            .where(subtree.c.id == new_parent_id)  # type: ignore[arg-type]
            .exists()
        )
        result = await self.session.execute(query)
        return result.scalar()

    async def update_department(self, department_id: int, data: dict):
        try:
            return await self.update(
                DepartmentUpdate(**data), exclude_unset=True, id=department_id
            )

        except IntegrityError as e:
            await self.session.rollback()
            if isinstance(e.orig.__cause__, UniqueViolationError):
                raise DepartmentNameExistsException()
            else:
                raise

    async def delete_department_cascade(self, department_id: int):
        await self.delete(id=department_id)

    async def delete_department_reassign(self, department_id: int, reassign_to_department_id: int):
        stmt = (
            update(Employee)
            .where(Employee.department_id == department_id)
            .values(department_id=reassign_to_department_id)
        )
        await self.session.execute(stmt)
        await self.session.execute(delete(self.model).where(self.model.id == department_id))
        await self.session.commit()
