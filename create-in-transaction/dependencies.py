from db import LocalSession


def get_session():
    session = LocalSession()
    yield session
    session.close()
