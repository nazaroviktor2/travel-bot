import uuid

from sqlalchemy import UUID, Integer
from sqlalchemy.orm import Mapped, mapped_column

from webapp.models.meta import Base


class ApiKey(Base):
    __tablename__ = "api_key"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)

    key: Mapped[uuid.UUID] = mapped_column(UUID, default=uuid.uuid4)
