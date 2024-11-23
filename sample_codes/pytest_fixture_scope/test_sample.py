import pytest


@pytest.fixture(scope="module")
def db():
    db = []
    yield db
    del db

def test_empty(db):
    assert len(db) == 0


def test_non_empty(db):
    db.append("dog")
    db.append("cat")
    assert len(db) == 2

def test_non_empty_again(db):
    assert len(db) == 0