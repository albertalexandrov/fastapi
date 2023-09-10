from fastapi import APIRouter, Depends

from dependencies import create_object_use_case, get_object_use_case, update_object_use_case, delete_object_use_case
from repositories import CountriesRepository
from schemas import CreateCountry, Country, UpdateCountry
from usecases import CreateObjectUseCase, GetObjectUseCase, UpdateObjectUseCase, DeleteObjectUseCase

router = APIRouter()


@router.post("/countries", response_model=Country)
def create_country(
    create_data: CreateCountry, use_case: CreateObjectUseCase = Depends(create_object_use_case(CountriesRepository))
):
    return use_case.create(create_data=create_data.model_dump())


@router.get("/countries/{country_id}", response_model=Country)
def get_country(country_id: int, use_case: GetObjectUseCase = Depends(get_object_use_case(CountriesRepository))):
    return use_case.get_object_or_404(pk_value=country_id)


@router.patch("/countries/{country_id}", response_model=Country)
def update_country(
    country_id: int,
    update_data: UpdateCountry,
    use_case: UpdateObjectUseCase = Depends(update_object_use_case(CountriesRepository))
):
    return use_case.update_object_or_404(pk_value=country_id, update_data=update_data.model_dump(exclude_unset=True))


@router.delete("/countries/{country_id}")
def delete_country(
    country_id: int, use_case: DeleteObjectUseCase = Depends(delete_object_use_case(CountriesRepository))
):
    use_case.delete_object_or_404(pk_value=country_id)

    return "Country was deleted"
