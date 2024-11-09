---
title: "Pythonのgeneratorの動作イメージを理解する"
emoji: "🐈"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["python", "generator"]
published: true
---

Pythonのgeneratorは強力な機能で、使いこなせるようになるとコーディングの幅が広がります。
一方で動作イメージが掴みにくいものでもあります。本記事ではgeneratorの動作原理を解説します。

あくまで動作イメージを理解するためのもので、generatorの実践的な使い方や応用については他の記事を参照してください。

## generatorの基本

generatorは、iteratorの一種で、`yield`キーワードを使用して値を一つずつ返す関数です。通常の関数とは異なり、値を返した後も関数の状態（ローカル変数や実行位置）が保持され、次回の呼び出し時にその続きから実行されます。pythonでは関数定義の中に`yield`があると、その関数はgeneratorとして扱われます。

例えば以下のようなものがgeneratorです。

```python
def three_sequence():
    yield 0
    yield 1
    yield 2
```

通常の関数は`return`で値を返しますが、generatorは`yield`で値を返します。さらに、`yield`で値を返すと、その時点で処理を抜け、次回の呼び出し時には前回の続きから実行されます。

また、通常の関数は`func_name()`で実行して戻り値を受け取りますが、generatorは`generator_name()`でgeneratorオブジェクトを作成した後、`next(generatorオブジェクト)`で値を取得します。

※ `next()`はiteratorから次の要素を取得する組み込み関数です。なのでgeneratorオブジェクトはiteratorです

以下のようにしてgeneratorから値を取得できます。
```python
gen = three_sequence()  # generatorオブジェクトを作成

print(next(gen))  # >> 0
print(next(gen))  # >> 1
print(next(gen))  # >> 2
```

`three_sequence`は`0`から`2`までの整数を返すgeneratorなので、`next()`を呼び出すたびに`0`、`1`、`2`が順番に出力されます。
4回目以降の`next()`を呼び出すと`StopIteration`エラーが発生します。

内部の動作イメージを詳しく説明すると以下のようになります。

1. `gen = three_sequence()`でgeneratorオブジェクトが作成される
2. `next(gen)`でgeneratorが実行され、`yield 0`で`0`が返される
3. `next(gen)`でgeneratorが再開され、`yield 1`で`1`が返される
4. `next(gen)`でgeneratorが再開され、`yield 2`で`2`が返される

## generatorで無限に値を返す

先ほどの例では3つの値を返すgeneratorでしたが、さらに動作イメージを掴むために、無限に値を返すgeneratorを見てみます。

```python
def infinite_sequence():
    num = 0
    while True:
        print(f"\t In generator before yield: {num}")
        yield num
        print(f"\t In generator after yield: {num}")
        num += 1
```

このgeneratorは`0`から始まり、`1`、`2`、`3`...と無限に整数を返します。

以下のようにして実行するとどうなるか考えてみてください。

```python
gen = infinite_sequence()

print("next(gen)0:")
out = next(gen)
print(f"out: {out}")
print()

print("next(gen)1:")
out = next(gen)
print(f"out: {out}")
print()

print("next(gen)2:")
out = next(gen)
print(f"out: {out}")
print()
```

上記を実行すると以下のような出力になります。

```txt
next(gen)0:
	In generator before yield: 0
out: 0

next(gen)1:
	In generator after yield: 0
	In generator before yield: 1
out: 1

next(gen)2:
	In generator after yield: 1
	In generator before yield: 2
out: 2
```

動作イメージが掴めるでしょうか？
ポイントは、`yield`で値を返して処理を抜け、次回の呼び出し時に前回の続きから処理を再開することです。
コードに合わせてコメントで説明を追加すると以下のようになります。

```python
def infinite_sequence():
    num = 0  # 処理1
    while True:
        print(f"\t In generator before yield: {num}")  # 処理2
        yield num  # 処理3(numを返して処理を抜ける)
        print(f"\t In generator after yield: {num}")  # 処理4
        num += 1  # 処理5

gen = infinite_sequence()

print("next(gen)0:")  # next(gen)0: と表示
out = next(gen)       # 処理1から処理3まで実行
print(f"out: {out}")  # out: 0 と表示
print()               # 改行

print("next(gen)1:")  # next(gen)1: と表示
out = next(gen)       # infinite_sequenceの中に入り、前回の続きを実行するので、処理4,5,2,3まで実行
print(f"out: {out}")  # out: 1 と表示
print()
```

以上でgeneratorの動作イメージを理解できたかと思います。

## 【参考】 generatorの使いどころ

どういった場面でgeneratorが役に立つのかについては[How to Use Generators and yield in Python](https://realpython.com/introduction-to-python-generators/)にいい例があったのでそのまま引用します。

---

Have you ever had to work with a dataset so large that it overwhelmed your machine’s memory? Or maybe you have a complex function that needs to maintain an internal state every time it’s called, but the function is too small to justify creating its own class. In these cases and more, generators and the Python yield statement are here to help.

マシンのメモリを圧迫するほど大きなデータセットを扱ったことがあるだろうか？ あるいは、呼び出されるたびに内部状態を維持する必要がある複雑な関数があるかもしれませんが、その関数は小さすぎて、独自のクラスを作ることはできません。 このような場合、ジェネレータと Python の yield 文が役に立ちます。

---
