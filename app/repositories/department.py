from loguru import logger
from sqlalchemy import select, update, delete, literal
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import aliased
from sqlalchemy.exc import IntegrityError

from app.models.employee import Employee
from app.models.department import Department
from app.repositories.base import BaseRepository
from app.schemas import DepartmentCreate
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

    async def get_department_tree(self, department_id: int, max_depth: int):
        """
        WITH RECURSIVE subtree AS (
            SELECT id, name, parent_id, created_at, 0 AS depth
            FROM departments
            WHERE id = :department_id

            UNION ALL

            SELECT d.id, d.name, d.parent_id, d.created_at, s.depth + 1
            FROM departments d
            JOIN subtree s ON d.parent_id = s.id
            WHERE s.depth < :max_depth
        )
        SELECT * FROM subtree
        """
        subtree = (
            select(
                Department.id,
                Department.name,
                Department.parent_id,
                Department.created_at,
                literal(0).label("depth"),
            )
            .where(Department.id == department_id)
            .cte(name="subtree", recursive=True)
        )

        depart = aliased(Department)

        subtree = subtree.union_all(
            select(
                depart.id,
                depart.name,
                depart.parent_id,
                depart.created_at,
                (subtree.c.depth + 1).label("depth"),
            )
            .join(subtree, depart.parent_id == subtree.c.id)
            .where(subtree.c.depth < max_depth)
        )

        result = await self.session.execute(select(subtree))
        return result.mappings().all()

    async def get_employees_by_departments(self, department_ids: list[int]):
        stmt = (
            select(Employee)
            .where(Employee.department_id.in_(department_ids))
            .order_by(Employee.created_at)
        )
        result = await self.session.execute(stmt)
        return result.scalars().all()

    async def create_department(self, data: DepartmentCreate):
        try:
            return await self.create(data)

        except IntegrityError as e:
            await self.session.rollback()
            logger.warning(
                f"Ошибка в создании подразделения: {e.orig.__cause__.__class__.__name__}"
            )
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
            stmt = (
                update(self.model)
                .where(self.model.id == department_id)
                .values(**data)
                .returning(self.model)
            )
            result = await self.session.execute(stmt)
            await self.session.commit()
            return result.scalar_one_or_none()

        except IntegrityError as e:
            await self.session.rollback()
            logger.warning(
                f"Ошибка обновления подразделения: {e.orig.__cause__.__class__.__name__}"
            )
            if isinstance(e.orig.__cause__, UniqueViolationError):
                raise DepartmentNameExistsException()
            else:
                raise

    async def delete_department_cascade(self, department_id: int):
        await self.delete(id=department_id)

    async def delete_department_reassign(
        self, department_id: int, reassign_to_department_id: int
    ):
        stmt = (
            update(Employee)
            .where(Employee.department_id == department_id)
            .values(department_id=reassign_to_department_id)
        )
        await self.session.execute(stmt)
        await self.session.execute(
            delete(self.model).where(self.model.id == department_id)
        )
        await self.session.commit()
