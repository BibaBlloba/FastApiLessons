from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from src.database import Base


class UsersOrm(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(200))
    last_name: Mapped[str] = mapped_column(String(200))
    login: Mapped[str] = mapped_column(String(200))

    email: Mapped[str] = mapped_column(String(200))
    passowrd: Mapped[str] = mapped_column(String(200))
