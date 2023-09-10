# Подход к разработке на FastAPI

В данном репозитории описаны мой подход к разработке на FastAPI, которые сформировались в ходе изучения данного 
фреймворка, чтения различных материалов в интернете и изучения принципов чистой архитектуры, и, собственно,
написания сервисов

```
Дисклеймер

Поскольку на FastAPI мною написаны откровенно небольшие сервисы, описанные подходы возможно не подойдут для больших
сервисов. В любом случае буду стараться дополнять подходы по мере их развития.
```

Итак, подход. Подход является урезанной версией чистой архитектуры (возможно, громко сказано).
Выделяются три слоя: 
1. вьюхи, 
2. пользовательские сценарии (use case в терминологии чистой архитектуры) и
3. репозитории (которые в терминологии вроде называются gateway и вроде как на самом деле являются data source, 
но этот вопрос еще нужно изучить)

## use case

use case - это callable. Я использую класс с единственным методом, например:

```python
from typing import Any

from fastapi import HTTPException
from starlette import status


class DoesNotExist(Exception):
    pass


class Repository:
    
    def get(self, pk_value: Any): pass


class Http404(HTTPException):

    def __init__(self, message: str = "Объект не найден"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)


class GetObjectUseCase:
    """Пользовательский кейс получения объекта."""
    
    def __init__(self, repo: Repository):
        self._repo = repo

    def get_object_or_404(self, pk_value: Any):
        try:
            instance = self._repo.get(pk_value)
        except DoesNotExist:
            raise Http404

        return instance
```

Подобная гранулярность кажется мне хорошим подходом, тк количество кода невелико, 
соблюдается принцип единственной ответственности, легко тестируется, переиспользуется
(особенно в случае с CRUD-операциями - представленный выше пользовательский кейс можно
использовать с разными вьюхами). Главное, как мне кажется, такой подход позволяет
сосредоточиться на одной задачи. 

В модуле [usecases.py](crud-without-list/usecases.py) представлены простые пользовательские сценарии 
для работы с одной моделью данных (не нужна транзакция): создать объект, получить, обновить и удалить.

## Репозитории

Реализуют доступ к источнику данных. Мой вариант репозитория:

```python
from typing import Any

from sqlalchemy import select, func, BinaryExpression
from sqlalchemy.orm import Session


class DoesNotExist(Exception):
    pass


class MultipleObjectsReturned(Exception):
    pass


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
```


## 1. CRUD-приложение

Пусть необходимо создать простое CRUD-приложение справочник стран. 
Приложение должно предоставлять возможность:

- создать, 
- получить информацию по идентификатору, 
- обновить и 
- удалить.

Получение простого и пагинированного списков будет рассмотрено отдельно.

Реализацию вместе необходимыми пояснениями см. в папке [crud-without-list](crud-without-list). 