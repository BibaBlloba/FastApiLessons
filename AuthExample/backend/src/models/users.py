from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    nickname: Mapped[str] = mapped_column(String(30), unique=True)
    email: Mapped[str | None] = mapped_column(unique=True)
    hashed_password: Mapped[str]
