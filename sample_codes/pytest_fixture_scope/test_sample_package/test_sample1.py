
def test_empty(db):
    assert len(db) == 0


def test_non_empty(db):
    db.append("dog")
    db.append("cat")
    assert len(db) == 2