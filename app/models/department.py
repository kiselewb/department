from datetime import datetime

from sqlalchemy import String, ForeignKey, DateTime, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Department(Base):
    __tablename__ = "departments"

    __table_args__ = (
        UniqueConstraint("parent_id", "name", name="uq_department_name_per_parent"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    parent_id: Mapped[int | None] = mapped_column(ForeignKey("departments.id", ondelete="CASCADE"), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    parent: Mapped["Department | None"] = relationship(
        "Department",
        back_populates="children",
        remote_side="Department.id",
    )
    children: Mapped[list["Department"]] = relationship(
        "Department",
        back_populates="parent",
        cascade="all, delete-orphan",
    )
    employees: Mapped[list["Employee"]] = relationship(
        "Employee",
        back_populates="department",
        cascade="all, delete-orphan",
    )

    def __repr__(self) -> str:
        return f"<Department id={self.id} name={self.name!r} parent_id={self.parent_id}>"
