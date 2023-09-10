from typing import TypeVar, Generic

from fastapi import Query, Depends
from fastapi_filter.contrib.sqlalchemy import Filter
from pydantic import Field, AnyUrl
from pydantic.generics import GenericModel
from sqlalchemy import select, func, Select
from sqlalchemy.orm import Session
from starlette.requests import Request

from dependencies import get_session

M = TypeVar('M')


class PaginatedResponse(GenericModel, Generic[M]):
    count: int = Field(description='Общее количество записей')
    next: AnyUrl | None = Field(description="Ссылка на следующую страницу")
    previous: AnyUrl | None = Field(description="Ссылка на предыдущую страницу")
    results: list[M] = Field(description='Результат')


class PageNumberPagination:
    """Пагинатор.

    Notes:
        Здесь обходимся без репозиториев, тк по моему мнению репозиторий не должен работать
        с фильтрами fastapi_filter.Filter
        Предлагается рассматривать пагинатор как частный случай пользовательского кейса (use case)

    """

    max_results = 100

    def __init__(self, request: Request, page: int = Query(1, gt=0), page_size: int = Query(10, gt=0),
                 session: Session = Depends(get_session)):
        self._page = page
        self._page_size = page_size if page_size <= self.max_results else self.max_results
        self._request = request
        self._session = session

    def get_page(self, filters: Filter, stmt: Select):
        """Возвращает результат пагинации в соответствии с фильтрами.

        Args:
            filters: фильтры
            stmt: sql-запрос

        """

        stmt = filters.filter(stmt)
        stmt = filters.sort(stmt)

        count = self._get_count(stmt)

        return {
            'count': count,
            'next': self._get_next_page(count),
            'previous': self._get_previous_page(count),
            'results': self._get_results(stmt)
        }

    def _get_count(self, stmt: Select):
        """Возвращает общее количество элементов.

        Args:
            stmt: sql-запрос

        """

        count = self._session.scalar(select(func.count()).select_from(stmt.subquery()))

        return count

    def _get_next_page(self, count: int) -> str:
        """Возвращает ссылку на следующую страницу.

        Args:
            count: общее количество элементов

        """

        total_pages = self._get_total_pages(count)

        if self._page >= total_pages:
            return

        url = self._request.url.include_query_params(page=self._page + 1)

        return str(url)

    def _get_previous_page(self, count: int) -> str:
        """Возвращает ссылку на предыдущую страницу.

        Args:
            count: общее количество элементов

        """

        total_pages = self._get_total_pages(count)

        if not (1 < self._page <= total_pages):
            return

        url = self._request.url.include_query_params(page=self._page - 1)

        return str(url)

    def _get_total_pages(self, count: int) -> int:
        """Возвращает количество страниц.

        Args:
            count: общее количество элементов

        """

        return count // self._page_size + 1

    @property
    def offset(self):
        """Возвращает смещение."""
        return (self._page - 1) * self._page_size

    def _get_results(self, stmt: Select) -> list[M]:
        """Возвращает объекты.

        Args:
            stmt: sql-запрос

        """

        stmt = stmt.limit(self._page_size).offset(self.offset)
        results = self._session.scalars(stmt)

        return results.all()
