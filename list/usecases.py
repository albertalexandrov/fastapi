from fastapi import Depends
from fastapi_filter.contrib.sqlalchemy import Filter
from sqlalchemy import Select
from sqlalchemy.orm import Session

from dependencies import get_session


class ListObjectsUseCase:
    """Пользовательский кейс получения непагинированного списка объектов.

    Notes:
        Здесь обходимся без репозиториев, тк по моему мнению репозиторий не должен работать
        с фильтрами fastapi_filter.Filter
        Для получения пагинированного списка объектов используйте PageNumberPagination

    """

    def __init__(self, session: Session = Depends(get_session)):
        self._session = session

    def list_objects(self, filters: Filter, stmt: Select) -> list:
        """Возвращает список объектов.

        Args:
            filters: фильтры
            stmt: sql-запрос

        """

        stmt = filters.filter(stmt)
        stmt = filters.sort(stmt)
        results = self._session.scalars(stmt)

        return results.all()
