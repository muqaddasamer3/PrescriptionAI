from typing import TYPE_CHECKING
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship, mapped_column, Mapped
from app.database.base import Base
import uuid
from uuid import UUID

if TYPE_CHECKING:
    from .prescription import Prescription

class User(Base):
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)

    # Relationships
    prescriptions: Mapped[list["Prescription"]] = relationship(
        "Prescription", back_populates="user", cascade="all, delete-orphan"
    )