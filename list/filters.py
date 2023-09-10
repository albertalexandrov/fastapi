from fastapi_filter.contrib.sqlalchemy import Filter

from models import Country


class CountriesFilter(Filter):
    """Фильтры стран."""

    id__in: list[int] | None
    name__ilike: str | None
    code: str | None

    ordering: list[str] | None = ["name"]

    class Constants(Filter.Constants):
        model = Country
        ordering_field_name: str = "ordering"
