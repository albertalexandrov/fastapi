from pydantic import BaseModel


class CitySchema(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class CountrySchema(BaseModel):
    id: int
    name: str
    iso: str
    cities: list[CitySchema]

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
