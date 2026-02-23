from collections import defaultdict
from typing import Sequence

from loguru import logger

from app.models import Department
from app.repositories.department import DepartmentRepository
from app.schemas import DepartmentCreate, DepartmentUpdate
from app.schemas.department import DepartmentDeleteMode, DepartmentTree
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

    async def get_departments(self) -> Sequence[Department]:
        return await self.repository.get_all()

    async def get_department_by_id(
        self, department_id: int, depth: int, include_employees: bool
    ) -> DepartmentTree:
        logger.info(
            f"Получение подразделения id={department_id}, глубина={depth}, вывод работников={include_employees}"
        )
        rows = await self.repository.get_department_tree(department_id, depth)

        if not rows:
            logger.warning("Ошибка получения - подразделение не найдено")
            raise DepartmentNotFoundException()

        if include_employees:
            department_ids = [row["id"] for row in rows]
            employees = await self.repository.get_employees_by_departments(
                department_ids
            )

            employees_tree = defaultdict(list)
            for emp in employees:
                employees_tree[emp.department_id].append(emp)

            logger.info("Дерево подразделения с работниками получено")
            return DepartmentTree(**self._build_tree(rows, employees_tree))
        else:
            logger.info("Дерево подразделения получено")
            return DepartmentTree(**self._build_tree(rows))

    async def create_department(self, data: DepartmentCreate) -> Department:
        logger.info(f"Создание подразделения: {data.model_dump()}")
        result = await self.repository.create_department(data)
        logger.info(f"Подразделение создано: {result!r}")
        return result

    async def update_department(
        self, department_id: int, data: DepartmentUpdate
    ) -> Department:
        logger.info(f"Обновление подразделения id={department_id}, {data.model_dump()}")
        new_department_data = data.model_dump(exclude_unset=True)

        if not new_department_data:
            logger.warning(
                "Ошибка обновления подразделения - данные для изменения не указаны"
            )
            raise RequestBodyRequiredException()

        if not await self.repository.get_one_or_none(id=department_id):
            logger.warning(
                f"Ошибка обновления - подразделение не найдено, id={department_id}"
            )
            raise DepartmentNotFoundException()

        if "parent_id" in new_department_data:
            new_parent_id = new_department_data.get("parent_id")

            if new_parent_id is not None:
                if new_parent_id == department_id:
                    logger.warning(
                        f"Ошибка обновления - подразделение не может быть родителем самому себе, id=parent_id={new_parent_id}"
                    )
                    raise DepartmentNotSelfParentException()

                if not await self.repository.get_one_or_none(id=new_parent_id):
                    logger.warning(
                        f"Ошибка обновления - родительское подразделение не найдено, parent_id={new_parent_id}"
                    )
                    raise ParentDepartmentNotFoundException()

                if await self.repository.is_department_descendant(
                    department_id, new_parent_id
                ):
                    logger.warning(
                        f"Ошибка обновления - цикл в дереве подразделений, id={department_id} parent_id={new_parent_id}"
                    )
                    raise DepartmentCycleException()

        logger.info(
            f"Подразделение успешно обновлено. id={department_id} new_data={new_department_data}"
        )
        return await self.repository.update_department(
            department_id, new_department_data
        )

    async def delete_department(
        self, department_id: int, mode: str, reassign_to_department_id: int | None
    ) -> None:
        logger.info(
            f"Удаление подразделения id={department_id}, mode={mode}, new_parent_id={reassign_to_department_id}"
        )
        if not await self.repository.get_one_or_none(id=department_id):
            logger.warning(
                f"Ошибка удаления - подразделение не найдено, id={department_id}"
            )
            raise DepartmentNotFoundException()

        if mode == DepartmentDeleteMode.reassign and reassign_to_department_id is None:
            logger.warning("Ошибка удаления - поле reassign_to_department_id не задано")
            raise ReassignModeException()

        if mode == DepartmentDeleteMode.reassign:
            if reassign_to_department_id == department_id:
                logger.warning(
                    "Ошибка удаления - reassign_to_department_id равно department_id"
                )
                raise ReassignToSelfException()

            if not await self.repository.get_one_or_none(id=reassign_to_department_id):
                logger.warning(
                    f"Ошибка удаления - новое подразделение не найдено reassign_to_department_id={reassign_to_department_id}"
                )
                raise TargetDepartmentNotFoundException()

            await self.repository.delete_department_reassign(
                department_id, reassign_to_department_id
            )
        else:
            await self.repository.delete_department_cascade(department_id)

        logger.info(
            f"Успешное удаление подразделения id={department_id} в режиме {mode}"
        )

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
