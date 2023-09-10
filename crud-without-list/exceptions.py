from fastapi import HTTPException
from starlette import status


class DoesNotExist(Exception):
    pass


class MultipleObjectsReturned(Exception):
    pass


class Http404(HTTPException):

    def __init__(self, message: str = "Объект не найден"):
        super().__init__(status_code=status.HTTP_404_NOT_FOUND, detail=message)
