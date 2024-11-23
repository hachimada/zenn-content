import pytest

@pytest.fixture(scope="package")
def db():
    db = []
    yield db
    del db