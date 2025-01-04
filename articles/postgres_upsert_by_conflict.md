---
title: "Postgresqlで`ON CONFLICT`を使ってupsertをする"
emoji: "🕌"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["postgresql", "database",]
published: true
---

PostgreSQLにおける**UPSERT**は、`ON CONFLICT`句を使用して実現できます。本記事では、UPSERTの基本から`ON CONFLICT`を使った具体的な使用例まで、段階を追って説明します。

---

## 1. UPSERTとは？

**UPSERT**は、「UPDATE」と「INSERT」を組み合わせた造語で、データベース操作において、指定した条件に基づき、既存のレコードを更新（UPDATE）するか、新しいレコードを挿入（INSERT）するかを自動的に判断して実行する操作を指します。これにより、複数のクエリを実行する必要がなくなり、処理の効率化とコードの簡潔化が図れます。

---

## 2. なぜUPSERTが必要か？

### 背景

データベースに新しいデータを挿入する際、既に同じキー（例えば主キーやユニーク制約が設定されているカラム）を持つレコードが存在する場合、単純な`INSERT`文ではエラーが発生します。このような状況では、次のような対応が必要です

1. **事前に存在確認を行う**：`SELECT`文で既存のレコードを確認し、存在すれば`UPDATE`、存在しなければ`INSERT`する。
2. **トランザクションを使用する**：複数のクエリをトランザクション内で実行し、一貫性を保つ。

しかし、これらの方法は手間がかかり、パフォーマンスにも影響を与える可能性があります。

### 解決する課題

`UPSERT`を使用することで、以下の課題を解決できます

- **クエリの簡素化**：1つのクエリで挿入と更新を同時に処理。
- **パフォーマンス向上**：不要な`SELECT`やトランザクションを回避。
- **コードの可読性向上**：より直感的なデータ操作が可能。

---

## 3. PostgreSQLにおけるUPSERTの実装方法

PostgreSQLでは、`INSERT ... ON CONFLICT`構文を使用してUPSERTを実現します。

### ステップ1：テーブルの作成

まず、サンプルとなるテーブルを作成します。ここでは、ユーザー情報を管理する`users`テーブルを考えます。

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

- `id`：自動増分の主キー。
- `username`：ユニーク制約が設定されており、一意のユーザー名が必要。
- `email`：ユーザーのメールアドレス。
- `created_at`：レコード作成時のタイムスタンプ。

### ステップ2：通常のINSERT文

新しいユーザーを挿入する際の通常の`INSERT`文は以下の通りです。

```sql
INSERT INTO users (username, email) VALUES ('alice', 'alice@example.com');
```

### ステップ3：UPSERTの実装（ON CONFLICTを使用）

既に存在する`username`に対して挿入を試みると、ユニーク制約によりエラーが発生します。この競合が発生した時にどうするかを`ON CONFLICT`を使って指定できます

#### 例1：競合時に何もしない（DO NOTHING）

```sql
INSERT INTO users (username, email) 
VALUES ('alice', 'alice_new@example.com')
ON CONFLICT (username) DO NOTHING;
```

- `username`が既に存在する場合、挿入をスキップし、何も行いません。

#### 例2：競合時に既存のレコードを更新（DO UPDATE）

```sql
INSERT INTO users (username, email) 
VALUES ('alice', 'alice_new@example.com')
ON CONFLICT (username) 
DO UPDATE SET email = EXCLUDED.email, created_at = CURRENT_TIMESTAMP;
```

- `username`が既に存在する場合、`email`を新しい値に更新し、`created_at`を現在のタイムスタンプに更新します。
- `EXCLUDED`は、挿入しようとした新しい値を参照しています

---

## 4. まとめ

`UPSERT`を活用することで、データの挿入と更新を効率的に行うことが可能になります。特に、ユニーク制約が存在するカラムに対してデータを挿入する際に、既存のレコードを自動的に更新する必要がある場合に非常に有用です。Postgresqlでは`ON CONFLICT`句を使用することで実現でき、データベース操作のパフォーマンスとコードの可読性を向上させることができます。

**ポイントのまとめ**：

- **ON CONFLICT**：競合（ユニーク制約違反）が発生した場合の処理を指定。
  - `DO NOTHING`：何もせずにスキップ。
  - `DO UPDATE`：既存のレコードを更新。
- **EXCLUDED**：挿入しようとした新しい値を参照するキーワード。
