---
title: "pytestのfixtureのスコープとは"
emoji: "✨"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["pytest", "pytehon", "test"]
published: true
---

## fixtureのスコープとは

fixtureでは セットアップとティアダウンを定義することができます。
スコープはその**セットアップとティアダウンの実行するタイミングを決定する**役割を持ちます。

### `function`スコープ

説明するよりも、実際にコードを見てみましょう。`test_sample.py`というファイル名で以下のコードを作成します。

```python
import pytest

@pytest.fixture()
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
    db.append("dog")
    assert len(db) == 1

```

このコードでは、リストに値を保持するfixtureを`db`という名前で定義しています。
`db`は空のリストで初期化(セットアップ)され、テストが終わったらリストを削除(ティアダウン)しています。この処理は個々の関数ごとに行われるため、当たり前ですがこのテストは成功します。

ここで、--setup-showオプションを使ってテストのセットアップとティアダウンの順序を確認してみましょう。

```terminal
$ pytest --setup-show test_sample.py
test_sample.py 
        SETUP    F db
        pytest_fixture_scope/test_sample.py::test_empty (fixtures used: db).
        TEARDOWN F db
        SETUP    F db
        pytest_fixture_scope/test_sample.py::test_non_empty (fixtures used: db).
        TEARDOWN F db
        SETUP    F db
        pytest_fixture_scope/test_sample.py::test_non_empty_again (fixtures used: db).
        TEARDOWN F db
```

`pytest_fixture_scope/test_sample.py::test_XXX (fixtures used: db).`の前後に`SETUP`と`TEARDOWN`が実行されているのがわかります。
また、`F db`というのは`db`というfixtureが`function`スコープで実行(関数ごとに実行)されていることを示しています。

なので、先ほどのコードは、fixtureの定義を`@pytest.fixture(scope="function")`としていることと同じです。

### `module`スコープ

次に、`db`のスコープを`module`に変更してみましょう。

```python
@pytest.fixture(scope="module")  # ここを変更
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
    db.append("dog")
    assert len(db) == 1
```

すると先ほどのテストは失敗します。
`module`スコープにしたことで、`db`のセットアップとティアダウンはモジュール（.pyファイル）ごとに1回だけ実行されるようになり、`test_non_empty_again`の実行時には`test_non_empty`で追加したにはdogとcatが`db`に残っているため、`len(db) == 1`が失敗します。

`--setup-show`オプションを使ってテストのセットアップとティアダウンの順序を確認すると、確かに`db`のセットアップとティアダウンがモジュールごとに1回だけ実行されていることがわかります。また、`SETUP M db`のようにFがM(module)に変わっているのがわかります。

```terminal
test_sample.py 
    SETUP    M db
        pytest_fixture_scope/test_sample.py::test_empty (fixtures used: db).
        pytest_fixture_scope/test_sample.py::test_non_empty (fixtures used: db).
        pytest_fixture_scope/test_sample.py::test_non_empty_again (fixtures used: db)F
    TEARDOWN M db
```

なお、`test_non_empty_again(db)`で`assert len(db) == 3`のように変更すると、テストは成功します。

### `class`スコープ

`class`スコープでは、セットアップとティアダウンはクラスごとに実行されるようになります。

```python
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
```

--setup-showオプションを使ってテストのセットアップとティアダウンの順序を確認すると、確かに`db`のセットアップとティアダウンがクラスごとに1回だけ実行されていることがわかり、、`SETUP C db`のようにクラススコープであることがわかります。

```terminal
test_sample_class.py 
      SETUP    C db
        pytest_fixture_scope/test_sample_class.py::TestSampleClass1::test_empty (fixtures used: db).
        pytest_fixture_scope/test_sample_class.py::TestSampleClass1::test_non_empty (fixtures used: db).
      TEARDOWN C db
      SETUP    C db
        pytest_fixture_scope/test_sample_class.py::TestSampleClass2::test_non_empty_again (fixtures used: db).
      TEARDOWN C db
```

### `package`スコープ

packageスコープを指定すると、セットアップとティアダウンはパッケージごとに1回だけ実行されるようになります。例えば以下のような構造のパッケージがあるとします。

```txt
test_sample_package
├── conftest.py
├── test_sample1.py
└── test_sample2.py
```

conftest.pyは以下のようになっています。

```python
import pytest

@pytest.fixture(scope="package")
def db():
    db = []
    yield db
    del db
```

test_sample1.pyは以下のようになっています。

```python
def test_empty(db):
    assert len(db) == 0

def test_non_empty(db):
    db.append("dog")
    db.append("cat")
    assert len(db) == 2
```

test_sample2.pyは以下のようになっています。

```python
def test_non_empty_again(db):
    assert len(db) == 2
```

`--setup-show`オプションを使って実行順序を確認すると、確かに`db`のセットアップとティアダウンがパッケージ全体で1回だけ実行され、テストはすべて成功していることがわかります。また、`SETUP P db`のようにパッケージスコープであることがわかります。

```terminal
test_sample_package/test_sample1.py 
  SETUP    P db
        pytest_fixture_scope/test_sample_package/test_sample1.py::test_empty (fixtures used: db).
        pytest_fixture_scope/test_sample_package/test_sample1.py::test_non_empty (fixtures used: db).
test_sample_package/test_sample2.py 
        pytest_fixture_scope/test_sample_package/test_sample2.py::test_non_empty_again (fixtures used: db).
  TEARDOWN P db
```

### `session`スコープ

`session`スコープでは、セットアップとティアダウンはセッションごと（pytestを実行するとき）に1回だけ実行されるようになります。

### 注意点

- fixtureが他のfixtureに依存する場合は、依存先のfixtureのスコープが依存元のfixtureのスコープと同じかそれよりも広いスコープである必要があります。
- この記事では、`test_sample1.py`の後に`test_sample2.py`が実行されるなどように、テストの実行順に依存して`test_non_empty_again`が成功する例があります。わかりやすさのためにこのような例にしていますが、本来、**テストは実行順序に依存させるべきではない**ため、このような使い方は避けるべきです。
- 説明のしやすさのために、function → module → class → package → sessionの順に説明しましたが、スコープの広さは、小さい順にfunction → class → module → package → sessionです。
  
## 参考

- Brian Okken. テスト駆動Python 第2版 (Japanese Edition)
