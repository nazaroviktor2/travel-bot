from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.helpers import created_at, deleted_at, is_deleted
from webapp.models.meta import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column()

    items: Mapped[list["Item"]] = relationship("Item", back_populates="user")

    created_at: Mapped[created_at]
    deleted_at: Mapped[deleted_at]
    is_deleted: Mapped[is_deleted]
