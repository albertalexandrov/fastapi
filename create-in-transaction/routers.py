from fastapi import APIRouter, Depends

from schemas import CreateCountry, CountrySchema
from usecases import CreateCountryUseCase

router = APIRouter()


@router.post("/countries", response_model=CountrySchema)
def create_country(create_data: CreateCountry, use_case: CreateCountryUseCase = Depends()):
    """Создает страну и города."""

    return use_case.create_country(create_data=create_data.dict())
