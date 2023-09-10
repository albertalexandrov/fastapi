from fastapi import APIRouter, Depends
from fastapi_filter import FilterDepends
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from filters import CountriesFilter
from models import Country
from pagination import PageNumberPagination, PaginatedResponse
from schemas import CountrySchema
from usecases import ListObjectsUseCase

router = APIRouter()


@router.get("/not-paginated-countries", response_model=list[CountrySchema])
def get_not_paginated_countries(
    use_case: ListObjectsUseCase = Depends(), filters: CountriesFilter = FilterDepends(CountriesFilter)
):
    """Возвращает НЕпагинированный список стран.

    Тут важно не забыть ограничить количество (при пагинации используется значение по умолчанию)

    """

    # это выражение может быть разным как по форме, так и по сложности.  поэтому определение
    # выражения происходит здесь, а не где-нибудь еще.  к тому же так удобнее
    stmt = select(Country).options(selectinload(Country.cities)).limit(10)

    return use_case.list_objects(filters=filters, stmt=stmt)


@router.get("/paginated-countries", response_model=PaginatedResponse[CountrySchema])
def get_paginated_countries(
    paginator: PageNumberPagination = Depends(), filters: CountriesFilter = FilterDepends(CountriesFilter)
):
    """Возвращает пагинированный список стран."""

    # это выражение может быть разным как по форме, так и по сложности.  поэтому определение
    # выражения происходит здесь, а не где-нибудь еще.  к тому же так удобнее
    stmt = select(Country).options(selectinload(Country.cities))

    return paginator.get_page(filters=filters, stmt=stmt)
