from pydantic import BaseModel, Field


class CreateCountry(BaseModel):
    name: str
    iso: str


class Country(BaseModel):
    id: int
    name: str
    iso: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True


class UpdateCountry(BaseModel):
    name: str = Field(None)
    iso: str = Field(None)
