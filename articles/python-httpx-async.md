---
title: "httpxサクッと入門"
emoji: "🐍"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["python", "httpx", "async"]
published: true
---


本記事では、pythonで通信を行うときに、requestsなどは使ったことがあるけどhttpxは使ったことがない人向けに、「**httpx**」について入門的な内容を「基本的な使い方(同期処理)」「非同期処理」「エラーハンドリング」「その他機能」についてまとめています。また、非同期処理自体がわからない人でも理解できるように解説しています。

---

## 1. requests より httpx

### 1-1. requests の問題点

基本的に、Python で HTTP 通信をするときは**httpx**ライブラリを使うのが便利です。一方で、**requests** ライブラリを用いることもできます。しかし、requests は「同期的 (Synchronous) な通信」に特化しており、「非同期的 (Asynchronous) な通信」には対応していません。

そのため、requestsライブラリでは以下のような問題が発生します。

- 一度リクエストを送ると、その処理が完了するまで次の処理に進めない
- リクエストが多い（並行して大量に送信したい）とき、待ち時間が長くなる

そのため、下記のようなケースでは requests だけでは効率が悪く、httpx のような非同期処理に対応したライブラリが必要になります。

- 大量の外部 API にリクエストを送る
- マイクロサービス同士で多数の通信を短時間に処理する

### 1-2. httpx の特徴

1. **同期的にも非同期的にも利用できる**  
   - 1つのライブラリで、普通の「待つ」書き方も、async/await を使った「待たない」書き方も選べる。
2. **インターフェイスが比較的わかりやすい**  
   - requests ライブラリのような感覚で扱えるため、学習コストを抑えられる。
3. **よりモダンな HTTP 機能に対応**  
   - HTTP/2 や TLS (SSL) 周りの機能を使いやすい。

---

## 2. httpxの基本的な使い方

### 2-1. 簡単なリクエストの例

```python
import httpx

def fetch_data():
    # 同期版クライアントを生成
    with httpx.Client() as client:
        # GET リクエストを送る
        response = client.get("https://example.com")
        
        # ステータスコード確認 (200 OK など)
        print("Status:", response.status_code)
        
        # ボディのテキストを取得
        print("Response Body:", response.text)

if __name__ == "__main__":
    fetch_data()
```

#### ここでのポイント

- `httpx.Client()` を `with` 文で使うことで、自動的にリソース（コネクションなど）を開放しくれる
- 同期処理のため、`client.get()` が完了するまで次に進まない

### 2-2. POST リクエストやパラメータの指定など

```python
import httpx

def post_data():
    with httpx.Client() as client:
        data = {"key": "value"}
        response = client.post("https://example.com/api", json=data)
        print("Status:", response.status_code)
        print("Response:", response.json())

if __name__ == "__main__":
    post_data()
```

- `json=` 引数を使うことで JSON データを送信可能です。
- クエリパラメータを付与したい場合は `params` 引数を使います。

---

## 3. 非同期処理 (Asynchronous) の使い方

### 3-1. 非同期処理と同期処理の違い

- **同期処理**
  - Python コードが「処理が終わるまで次の処理に進まない」方式のことを指します。
  - 非同期処理を使ったことがない場合は、これまでのコードはほぼ同期処理だったと考えてOKです。
- **非同期処理**
  - 「ある処理が完了するのを待っている間に、他の処理を同時進行できる」やり方です。  
  - Python では `async` というキーワードを使って「非同期関数 (コルーチン)」を定義し、処理を待つ部分では `await` を使います。  
  - 非同期処理は、処理の完了を待たずにすぐ次の処理へ移るため、大量の HTTP リクエストを同時に実行し、結果を高速に集めたいときなどに便利です。

**非同期処理をあまり知らなくても最初は以下のポイントだけおさえておけばOK**

- `async def 関数名(...):` と書くと、その関数の中では `await` が使える
- `await` を付けて呼び出した箇所は、処理が終わるまで一旦「待つ」けれど、その待っている間に Python が他の「await」の処理も進めてくれる

### 3-2. 簡単な非同期の例

```python
import asyncio
import httpx

async def fetch_data_async():
    # 非同期版クライアントを生成
    async with httpx.AsyncClient() as client:
        response = await client.get("https://example.com")
        print("Status:", response.status_code)
        print("Response Body:", response.text)

async def main():
    # async 関数を呼び出すときに await が必要
    await fetch_data_async()

if __name__ == "__main__":
    # asyncio.run(...) を使うと、非同期関数(main)を「実行」できる
    asyncio.run(main())
```

#### ここでのポイント

- 非同期版クライアントは `httpx.AsyncClient()` を使う
- `async with ... as client:` と書くことで非同期クライアントを開き、終了時にきちんとクローズできる
- `await client.get(...)` とすることで、HTTP リクエストが終わるまで一旦待つが、他の非同期処理が並行して実行可能になる

### 3-3. 非同期が役に立つケース

- 多数のリクエストを行いたいとき
- リクエストを待っている時間を他の計算に使いたいとき

例えば、同時に複数の URL にアクセスしたい場合は下記のように書くことができます。

```python
import asyncio
import httpx

async def fetch_url(client, url):
    response = await client.get(url)
    return response.status_code, response.text

async def main():
    urls = [
        "https://example.com",
        "https://httpbin.org/get",
        # さらに複数のURLを追加
    ]
    async with httpx.AsyncClient() as client:
        # 複数の fetch_url 処理を同時に開始し gather でまとめて待つ
        tasks = [fetch_url(client, url) for url in urls]
        results = await asyncio.gather(*tasks)
        
    for i, (status, text) in enumerate(results):
        print(f"URL: {urls[i]}")
        print("Status:", status)
        print("Body length:", len(text))
        print("-------------")

if __name__ == "__main__":
    asyncio.run(main())
```

- `asyncio.gather` を使うと、複数の非同期関数 (コルーチン) (`fetch_url`) を一度に実行し、完了を待つことができます。
- 同期的に for ループで一つずつ処理するよりも高速に結果が返ってくる可能性があります。

---

## 4. エラー対応 (例外処理) の仕組み

### 4-1. エラー処理の例

同期・非同期ともに、httpx は内部的にタイムアウトや接続エラーなどの例外 (Exception) を投げる場合があります。基本的には `try ... except ...` で例外をキャッチして対応します。

```python
import httpx

def fetch_with_error_handling():
    try:
        with httpx.Client() as client:
            # タイムアウトを設定 (5秒でタイムアウト)
            response = client.get("https://example.com", timeout=5.0)
            response.raise_for_status()  # ステータスコードが4xx,5xxなら例外を投げる
            return response.text
    except httpx.TimeoutException:
        print("リクエストがタイムアウトしました")
    except httpx.HTTPStatusError as exc:
        print(f"HTTPエラーが発生しました。ステータスコード: {exc.response.status_code}")
    except httpx.RequestError as exc:
        print(f"接続エラーが発生しました。詳細: {exc}")

if __name__ == "__main__":
    result = fetch_with_error_handling()
    if result:
        print(result)
```

#### ここでのポイント

- `timeout=5.0` のように指定すると、サーバが 5 秒以内に応答しない場合は `httpx.TimeoutException` を発生させる
- `response.raise_for_status()` でステータスコードが 400 や 500 系の場合に `httpx.HTTPStatusError` が発生する
- それ以外にも `RequestError` をはじめ、さまざまな例外がある

### 4-2. 非同期でのエラー処理

非同期でも同様に `try ... except ...` を使います。例外のクラスも同じなので、同期とほぼ同じ書き方で対応できます。

```python
import asyncio
import httpx

async def fetch_async_with_error_handling():
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://example.com", timeout=5.0)
            response.raise_for_status()
            return response.text
    except httpx.TimeoutException:
        print("リクエストがタイムアウトしました (非同期)")
    except httpx.HTTPStatusError as exc:
        print(f"HTTPエラー (非同期)。ステータスコード: {exc.response.status_code}")
    except httpx.RequestError as exc:
        print(f"接続エラー (非同期)。詳細: {exc}")

async def main():
    result = await fetch_async_with_error_handling()
    if result:
        print(result)

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 5. その他の主な機能

### 5-1. 認証 (Basic 認証など)

```python
import httpx

def fetch_with_basic_auth():
    with httpx.Client(auth=("username", "password")) as client:
        response = client.get("https://example.com/protected")
        response.raise_for_status()
        return response.text
```

- `auth=("username", "password")` のように簡単にベーシック認証付きのサイトにアクセスできます。

### 5-2. Cookie の取り扱い

```python
import httpx

def fetch_with_cookies():
    with httpx.Client() as client:
        client.cookies.set("sessionid", "12345")
        response = client.get("https://example.com")
        return response.text
```

- Cookie の送受信を自動管理するので、ログイン後セッションを保持したいときに便利です。
