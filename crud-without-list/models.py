from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase


class Base(DeclarativeBase):
    pass


class Country(Base):
    """Модель страны."""

    __tablename__ = "country"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(comment="Наименование")
    iso: Mapped[str] = mapped_column(comment="Код ISO 3166-1")
