from fastapi import Depends
from sqlalchemy.orm import Session

from db import LocalSession
from usecases import CreateObjectUseCase, GetObjectUseCase, UpdateObjectUseCase, DeleteObjectUseCase


def get_session():
    session = LocalSession()
    yield session
    session.close()


def create_object_use_case(repository_kls):
    """Возвращает пользовательский сценарий создания объекта.

    Args:
        repository_kls: класс репозитория

    """

    def wrapper(session: Session = Depends(get_session)):
        repo = repository_kls(session)
        return CreateObjectUseCase(repo=repo)

    return wrapper


def get_object_use_case(repository_kls):
    """Возвращает пользовательский сценарий получения объекта.

    Args:
        repository_kls: класс репозитория

    """

    def wrapper(session: Session = Depends(get_session)):
        repo = repository_kls(session)
        return GetObjectUseCase(repo=repo)

    return wrapper


def update_object_use_case(repository_kls):
    """Возвращает пользовательский сценарий обновления объекта.

    Args:
        repository_kls: класс репозитория

    """

    def wrapper(session: Session = Depends(get_session)):
        repo = repository_kls(session)
        return UpdateObjectUseCase(repo=repo)

    return wrapper


def delete_object_use_case(repository_kls):
    """Возвращает пользовательский сценарий удаления объекта.

    Args:
        repository_kls: класс репозитория

    """

    def wrapper(session: Session = Depends(get_session)):
        repo = repository_kls(session)
        return DeleteObjectUseCase(repo=repo)

    return wrapper
