from sqlalchemy import ForeignKey, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from webapp.models.helpers import created_at, deleted_at, is_deleted
from webapp.models.meta import Base


class Item(Base):
    __tablename__ = "item"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column()
    note: Mapped[str] = mapped_column(nullable=True, default="")
    days_needed: Mapped[int] = mapped_column(Integer, index=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    user: Mapped["User"] = relationship("User", back_populates="items")

    created_at: Mapped[created_at]
    deleted_at: Mapped[deleted_at]
    is_deleted: Mapped[is_deleted]
