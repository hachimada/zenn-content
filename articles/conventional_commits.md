---
title: "整理されたコミットメッセージを書きたい！"
emoji: "🐥"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["git", "conventional-commits"]
published: true
---


## 問題意識

コミットメッセージ、ちゃんと書けていますか？

自分自身、他の人のコミットメッセージを見たりする中で、何となくこういう書き方が良いんだろうなというのは経験的にあったのですが、ちゃんと調べたことはなかったので、「Conventional Commits」というものについて調べて備忘録的にまとめてみました。

開発チームにはコミットメッセージに関する規約があれば、この記事は読まなくていいかもしれませんが、
規約は特になく各開発者の裁量に任せられていたり、もっと綺麗なコミットメッセージを書きたいと思っているのであれば参考になると思います。

綺麗なコミットメッセージを書いて、できるエンジニア感を醸し出しましょう。

## 1. Conventional Commits とは

Conventional Commits は、コミットメッセージに一貫性と明確さをもたらすための軽量な規約で、コミットメッセージを次のような標準フォーマットに沿って記述します。

```txt
<type>(<scope>): <subject>

<body>

<footer>
```

- **type**: コミットの種類を示すキーワード
  - feat: 新機能の追加
  - fix: バグ修正
  - docs: ドキュメントの変更
  - style: コードのフォーマットや見た目の変更（機能には影響しない）
  - refactor: リファクタリング（内部構造の改善）
  - perf: パフォーマンス改善
  - test: テストの追加や修正
  - chore: その他、補助的な変更
- **scope** (オプション): 変更が影響するモジュールや機能の範囲を示す。auth、ui、api など
- **subject**: 変更内容の概要を命令形で記述する。できるだけ簡潔に、50文字以内に収めることが推奨される
- **body** (オプション):　変更の背景や詳細な説明を記述する。内容が長くなる場合は、72文字程度で改行を入れると読みやすい
- **footer** (オプション): Breaking Change（後方互換性がない変更）や、関連するIssue番号などの追加情報を記述

※ type はここで挙げたものだけでなく、他のものも使用できますが、一般的に使われるものを挙げています。

## 2. Conventional Commits のメリット

- **一貫性のある履歴**
  - 全てのコミットが同じ形式で記述されるため、プロジェクトの変更履歴を簡単に追跡できる
- **自動化ツールとの連携**
  - コミットメッセージから changelog を自動生成したり、セマンティックバージョニング（SemVer）に基づいてバージョン管理を行うツールと連携しやすくなる
- **チーム内のコミュニケーション向上**
  - 各コミットに変更の目的や影響範囲が明確に記述されるため、チームメンバーが変更内容を素早く理解でき、レビューやメンテナンスが容易になる

## 3. 具体的なコミットメッセージの例

### 3-1. 新機能追加 (feat)

```txt
feat(auth): Add OAuth login functionality

Implemented OAuth login using Google and Facebook.
Closes #123
```

認証モジュール (auth) に OAuth ログイン機能を追加しています。関連する Issue (#123) もクローズしています。

### 3-2. バグ修正 (fix)

```txt
fix(api): Resolve null pointer error during data fetch

Fixed a null pointer error caused by misconfigured query settings.
Fixes #456
```

API でデータ取得時に発生していた null ポインターエラーを修正し、関連する Issue (#456) を解決しています。

### 3-3. ドキュメント更新 (docs)

```
docs(readme): Update installation instructions

Improved installation steps and added a troubleshooting section.
```

README に記載されているインストール手順を更新し、トラブルシューティングのセクションを追加する変更です。

### 3-4. リファクタリング (refactor)

```txt
refactor(ui): Simplify rendering logic for components

Removed duplicate code and improved readability and maintainability of UI components.
```

UI コンポーネントのレンダリングロジックをシンプルにし、重複するコードを削除することで、保守性を向上させるためのリファクタリングです。

### 3-5. Breaking Change

```txt
feat(api): Change user data response format

BREAKING CHANGE: The API response format has been changed from XML to JSON.
Clients must update their implementations accordingly.
```

API のユーザーデータのレスポンス形式を XML から JSON に変更したため、後方互換性がなく、利用しているクライアントは更新が必要となる旨を明記しています。

## ほんとに Conventional Commits が必要か

[Do all my contributors need to use the Conventional Commits specification?](https://www.conventionalcommits.org/en/v1.0.0/#do-all-my-contributors-need-to-use-the-conventional-commits-specification)にも書かれているように、全ての開発者がこの規約に従う必要はありません。

正直、規約に従うのは面倒臭かったり、ルールが多すぎて逆に混乱することもあるので、コミットメッセージを何らかのツールに連携させている場合などを除いけば、厳密に守る必要もないとは思います。

何をしたのか分かり易いコミットメッセージになっていれば良いので、Conventional Commits を**参考にしつつ**書いていけば良いかなと思っています。

最近はAIにコミットメッセージを生成してもらうこともできるので、AIにお任せするのも良いかもしれません。

## 参考リンク

- [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/)
