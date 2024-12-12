from sqlmodel import SQLModel, Field, DateTime
from datetime import datetime


class Base(SQLModel):
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(
        sa_type = DateTime,
        default_factory=datetime.now
    )
    updated_at: datetime = Field(
        sa_type = DateTime,
        sa_column_kwargs={"onupdate": datetime.now},
        nullable=True,
        default=None
    )


class Users(Base, table=True):
    __tablename__ = "users"
    name: str = Field(nullable=False)
    lastname: str = Field(nullable=False)
    dni: str = Field(nullable=False)
    phone: str = Field(nullable=True, default=None)
    email: str = Field(nullable=False)
