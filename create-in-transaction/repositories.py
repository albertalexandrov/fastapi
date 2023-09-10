from typing import Any

from sqlalchemy import select, func, BinaryExpression
from sqlalchemy.orm import Session

from exceptions import DoesNotExist, MultipleObjectsReturned
from models import Country, City


class Repository:
    model = None

    def __init__(self, session: Session):
        if self.model is None:
            raise ValueError(f'В классе {self.__class__.__name__} не определена модель model')

        self._session = session

    def create(self, create_data: dict, commit: bool = False, refresh: bool = False):
        """Создание объекта.

        Args:
            create_data: данные для создания объекта
            commit: флаг необходимости выполнить commit
            refresh: флаг необходимости выполнить refresh

        Флаги commit и refresh нужны для того, чтобы гибко управлять процессом создания вручную,
        тк не всегда нужно сразу коммитить изменения, например, если создание выполняется в транзакции
        и помимо прочего выполняется еще какая-либо операция, изменяющая состояние БД, и не всегда
        вообще требуется выполнять refresh

        """

        instance = self.model(**create_data)
        self._session.add(instance)

        if commit:
            self._session.commit()

            if refresh:
                self._session.refresh(instance)

        return instance

    def get(self, pk_value: Any = None, *whereclause: BinaryExpression):
        """Возвращает единственный объект по его первичному ключу или удовлетворяющего условиям поиска.

        Notes:
            Объект должен быть единственным

        Args:
            pk_value: значение первичного ключа
            whereclause: условия фильтрации

        Raises:
            DoesNotExist, если по условиям поиска не найдено ни одного объекта
            MultipleObjectsReturned, если по условиям поиска найдено более чем один объект

        """

        if pk_value is not None:
            instance = self._session.get(self.model, pk_value)

            if not instance:
                raise DoesNotExist

            return instance

        stmt = select(self.model).where(*whereclause)
        total = self._session.scalar(select(func.count()).select_from(stmt.subquery()))

        if total == 0:
            raise DoesNotExist

        if total > 1:
            raise MultipleObjectsReturned

        return self._session.scalar(stmt)

    def update(self, instance: object, update_data: dict, commit: bool = False, refresh: bool = False):
        """Обновляет объект.

        Args:
            instance: объект, который необходимо обновить
            update_data: данные, которыми необходимо обновить объект
            commit: флаг необходимости выполнить _commit
            refresh: флаг необходимости выполнения _refresh

        Raises:
            AttributeError, если ключ update_data не найден среди атрибутов instance

        """

        for field, value in update_data.items():
            setattr(instance, field, value)

        if commit:
            self._session.commit()

            if refresh:
                self._session.refresh(instance)

        return instance

    def delete(self, instance: object, commit: bool = False):
        """Удаляет объект.

        Args:
            instance: объект, который необходимо удалить
            commit: флаг необходимости выполнить commit

        """

        self._session.delete(instance)

        if commit:
            self._session.commit()


class CountriesRepository(Repository):
    model = Country


class CityRepository(Repository):
    model = City
