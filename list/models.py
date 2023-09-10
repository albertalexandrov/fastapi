from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase, relationship


class Base(DeclarativeBase):
    pass


class Country(Base):
    """Модель страны."""

    __tablename__ = "country"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(comment="Наименование")
    iso: Mapped[str] = mapped_column(comment="Код ISO 3166-1")
    cities: Mapped[list["City"]] = relationship(back_populates="country")


class City(Base):
    __tablename__ = "city"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(comment="Наименование")
    country_id: Mapped[int] = mapped_column(ForeignKey("country.id"))
    country: Mapped["Country"] = relationship(back_populates="cities")
