from fastapi import HTTPException
from starlette import status


class DoesNotExist(Exception):
    pass


class MultipleObjectsReturned(Exception):
    pass
