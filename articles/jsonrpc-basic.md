---
title: "JSON-RPC サクッと入門"
emoji: "👻"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["aiエージェント", "JSONRPC", "python"]
published: True
---


## JSON-RPC とは

JSON-RPC はリモートプロシージャコール (Remote Procedure Call; RPC) のシンプルなプロトコルで、JSON 形式を用いて通信します。クライアントは、呼び出したいメソッド名とそのパラメータを JSON オブジェクトとしてサーバーに送信し、サーバーはそのメソッドを実行して結果を返します。

つまり、ネットワーク越しにメソッド（関数）を呼び出し、その結果を受け取る仕組みです。また、現在広く使われているのは JSON-RPC 2.0 で、エラー処理やバッチリクエスト（同時に複数のリクエストを行う機能）などの仕様がしっかり定められています。

本記事に執筆時点（2025年4月）AI Agent開発でもこのJSON-RPCが注目されています。

Anthropicが2024年11月に発表した[MCP(Model Context Protocol)](https://github.com/modelcontextprotocol)は、LLMアプリケーションと外部データソースおよびツールとのシームレスな統合を可能にするオープンプロトコルですが、これはJSON-RPCを基にしています。

さらに、2025年4月にGoogleが発表した[Agent2Agent Protocol (A2A)](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)は、AIエージェント間の通信のためのプロトコルで、これもJSON-RPCを基にしています。

## JSON-RPCのリクエスト/レスポンスの構造

JSON-RPC のリクエストに含めるJSONは通常、以下のようなフィールドを持ちます

- jsonrpc: プロトコルバージョンを示すフィールド。例: "jsonrpc": "2.0"
- method: 呼び出す対象のメソッド名。例: "method": "subtract"
- params: メソッドに渡すパラメータ。通常は配列形式やオブジェクト形式が使われます。例: "params": [42, 23]
- id: リクエストに対する識別子。複数リクエストの区別やレスポンスとリクエストの関連付けに利用されます。

例:

```json
{
  "jsonrpc": "2.0",
  "method": "subtract",
  "params": [42, 23],
  "id": 1
}
```

一方、レスポンスは以下のような構造となります

- jsonrpc: バージョン情報（リクエストと同じく "2.0"）。
- result: 正常に処理された場合、実行結果が格納されるフィールド。
- error: エラーが発生した場合、エラーコードやメッセージが含まれるフィールド。
- id: リクエストの id と同じ値。これにより、どのリクエストに対するレスポンスかが分かります。

例:

```json
{
  "jsonrpc": "2.0",
  "result": 19,
  "id": 1
}
```

このように、JSON-RPC は一つのエンドポイントに対して一つの JSON オブジェクトを送ることで、リモートで関数を実行できる仕組みになっています。

## JSON-RPC エラーコード

以下は、よく使われる JSON-RPC のエラーコードとその意味です。

| コード    | メッセージ           | 説明                                                                                     |
| --------- | -------------------- | ---------------------------------------------------------------------------------------- |
| **-32700** | 解析エラー           | サーバーが無効な JSON を受信した場合に発生します。JSON テキストの解析中にエラーが起きた状況です。     |
| **-32600** | 無効なリクエスト       | 送信された JSON が有効な JSON-RPC リクエストオブジェクトではない場合に返されます。                     |
| **-32601** | メソッドが見つかりません | 指定されたメソッドが存在しないため、呼び出しが行えないときに返されるエラーです。                     |
| **-32602** | 無効なパラメータ       | 呼び出されたメソッドのパラメータが無効、もしくは不足している場合に返されます。                         |
| **-32603** | サーバーエラー         | サーバー側で実装エラーが発生した場合に予約されているエラーコードです。                             |

## サンプルコード

以下は、FastAPI と jsonrpc ライブラリを使って、シンプルな JSON-RPC サーバーを実装したサンプルコードです。このサンプルでは、基本的な四則演算（加算、減算、乗算、除算）の各メソッドをエンドポイントに登録し、curl コマンドからリクエストを送ると対応する計算処理が行われ、結果が返されるようになっています。

```python
from fastapi import FastAPI, Request
from jsonrpc import JSONRPCResponseManager, dispatcher
import uvicorn

app = FastAPI()

@dispatcher.add_method
def add(addend1: float, addend2: float) -> float:
    return addend1 + addend2

@dispatcher.add_method
def subtract(minuend: float, subtrahend: float) -> float:
    return minuend - subtrahend

@dispatcher.add_method
def multiply(multiplicand: float, multiplier: float) -> float:
    return multiplicand * multiplier

@dispatcher.add_method
def divide(dividend: float, divisor: float) -> float:
    if divisor == 0:
        raise ValueError("Division by zero is not allowed.")
    return dividend / divisor

@app.post("/api")
async def handle_rpc(request: Request) -> dict:

    # リクエストのバイトデータを取得し、文字列にデコードする
    body: bytes = await request.body()
    request_str: str = body.decode("utf-8")
    # JSON-RPC のリクエスト文字列を jsonrpc ライブラリで処理する
    response = JSONRPCResponseManager.handle(request_str, dispatcher)
    # レスポンスの data 部分を返却する
    return response.data

if __name__ == "__main__":
    # サーバーをホスト 0.0.0.0、ポート 8000 で起動する
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

1. dispatcher.add_method デコレーター
これを用いることで、JSON-RPC のリクエストで呼ばれる各メソッド（ここでは add、subtract、multiply、divide）を登録します。
各関数は引数として受け取る値の型（ここでは float）を指定しており、計算結果を返すシンプルな実装となっています。
1. JSONRPCResponseManager.handle:
渡された JSON 文字列と dispatcher に登録されたメソッド群を基に JSON-RPC のリクエストを処理し、レスポンスを生成します。
これにより、クライアントから送られたメソッド名とパラメータに対して、適切な処理が行われ結果が返されます。

### 動作確認

1. サーバーの起動:
上記スクリプトを実行すると、FastAPI サーバーがポート8000で起動します。
2. curl コマンドでのテスト:
以下のコマンドを実行することで、subtract メソッドの計算結果が得られます。

```bash
curl -X POST \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc": "2.0", "method": "subtract", "params": [42, 23], "id": 1}' \
  http://localhost:8000/api
```

以下のようなレスポンスが返ってきます。

```json
{
  "jsonrpc": "2.0",
  "result": 19,
  "id": 1
}
```

⸻

## 参考

- [JSON-RPC 2.0 Specification](https://www.jsonrpc.org/specification)
- [json-rpc](https://json-rpc.readthedocs.io/en/latest/)
