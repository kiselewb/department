from typing import TypeVar, Generic, Type, Sequence

from pydantic import BaseModel
from sqlalchemy import select, insert, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.base import Base


ModelType = TypeVar("ModelType", bound=Base)


class BaseRepository(Generic[ModelType]):
    def __init__(self, model: Type[ModelType], session: AsyncSession):
        self.model = model
        self.session = session

    async def get_all(self, *filter, **filter_by) -> Sequence[ModelType]:
        query = select(self.model).filter(*filter).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_one_or_none(self, **filter_by) -> ModelType | None:
        query = select(self.model).filter_by(**filter_by)
        result = await self.session.execute(query)
        return result.scalar_one_or_none()

    async def create(self, data: BaseModel) -> ModelType:
        stmt = insert(self.model).values(**data.model_dump()).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalars().one()

    async def delete(self, **filter_by) -> ModelType:
        stmt = delete(self.model).filter_by(**filter_by).returning(self.model)
        result = await self.session.execute(stmt)
        await self.session.commit()
        return result.scalars().one()
