import pytest


@pytest.fixture(scope="class")
def db():
    db = []
    yield db
    del db

class TestSampleClass1:
    def test_empty(self, db):
        assert len(db) == 0


    def test_non_empty(self, db):
        db.append("dog")
        db.append("cat")
        assert len(db) == 2

class TestSampleClass2:
    def test_non_empty_again(self, db):
        db.append("cat")
        assert len(db) == 1
        # assert len(db) == 3  # このテストは失敗する