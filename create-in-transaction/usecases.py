from fastapi import Depends
from sqlalchemy.orm import Session

from dependencies import get_session
from repositories import CityRepository, CountriesRepository


class CreateCountryUseCase:
    """Пользовательский кейс создания городов и стран.

    Более сложный кейс, тк создаются экземпляры двух моделей - соответственно нужна транзакция
    Для транзакции нужна одна-единственная сессия, которая будет передана в репозитории

    """

    def __init__(self, session: Session = Depends(get_session)):
        self._session = session
        self._cities_repo = CityRepository(session)
        self._countries_repo = CountriesRepository(session)

    def create_country(self, create_data: dict):
        cities = create_data.pop("cities")

        # здесь пригодится флаг commit=False, тк сейчас коммитить изменения в БД не нужно
        country = self._countries_repo.create(create_data)

        for city in cities:
            # здесь тоже не коммитим изменения
            city = self._cities_repo.create({"name": city})
            country.cities.append(city)

        self.commit()  # а здесь уже коммитим, тк все объекты добавлены в сессию
        self.refresh(country)

        return country

    def commit(self):
        self._session.commit()

    def refresh(self, instance: object):
        self._session.refresh(instance)
        return instance
