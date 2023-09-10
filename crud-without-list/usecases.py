from typing import Any

from exceptions import DoesNotExist, Http404
from repositories import Repository


class ActionUseCase:
    """Базовый пользовательский кейс."""

    def __init__(self, repo: Repository):
        self._repo = repo


class CreateObjectUseCase(ActionUseCase):
    """Пользовательский кейс по созданию объекта."""

    def create(self, create_data: dict):
        return self._repo.create(create_data, commit=True, refresh=True)


class GetObjectUseCase(ActionUseCase):
    """Пользовательский кейс получения объекта."""

    def get_object_or_404(self, pk_value: Any):
        try:
            instance = self._repo.get(pk_value)
        except DoesNotExist:
            raise Http404

        return instance


class UpdateObjectUseCase(ActionUseCase):
    """Пользовательский кейс обновления объекта."""

    def update_object_or_404(self, pk_value: Any, update_data: dict):
        try:
            instance = self._repo.get(pk_value)
        except DoesNotExist:
            raise Http404

        instance = self._repo.update(instance, update_data, commit=True, refresh=True)

        return instance


class DeleteObjectUseCase(ActionUseCase):
    """Пользовательский кейс удаления объекта."""

    def delete_object_or_404(self, pk_value: Any):
        try:
            instance = self._repo.get(pk_value)
        except DoesNotExist:
            raise Http404

        self._repo.delete(instance, commit=True)
