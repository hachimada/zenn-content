---
title: "pyproject.toml に Git リポジトリを追加する方法"
emoji: "🎉"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: []
published: false
---

# `pyproject.toml` で GitHub リポジトリを指定する方法

`pyproject.toml` では、Poetryを使って依存関係を管理する際に、GitHubのリポジトリを直接指定することが可能です。この時、特定のブランチ、タグ、またはコミットハッシュ、サブディレクトリを指定して取り込むことができます。

- **ブランチ指定**: 特定のブランチを依存関係として取り込む
- **タグ指定**: 安定したリリースバージョンを指定
- **コミットハッシュ指定**: 特定のコミットを依存関係とする
- **サブディレクトリ指定**: リポジトリ内の特定ディレクトリからインストール

## 基本的な構文

依存関係を追加する際には、`[tool.poetry.dependencies]` セクションに以下のように `git` キーを使用して指定します。

```toml
[tool.poetry.dependencies]
パッケージ名 = { git = "https://github.com/username/repo.git" }
```

### 1. 特定のブランチを指定する場合

`branch` キーを使用します。例えば、`main` ブランチを指定する場合は以下のように記述します。

```toml
[tool.poetry.dependencies]
package_name = { git = "https://github.com/username/repo.git", branch = "main" }
```

### 2. 特定のタグを指定する場合

`tag` キーを使用します。
安定したリリースバージョンを取り込みたいなどに便利です。

```toml
[tool.poetry.dependencies]
package_name = { git = "https://github.com/username/repo.git", tag = "v1.0.0" }
```

### 3. 特定のコミットハッシュを指定する場合

`rev` キーを使用します。対象のコミットハッシュ（例: `a1b2c3d4`）を指定します。

```toml
[tool.poetry.dependencies]
package_name = { git = "https://github.com/username/repo.git", rev = "commit_hash" }
```

### 4. リポジトリ内の特定のサブディレクトリからインストールする場合

モノリポジトリなど、リポジトリ内に複数のプロジェクトが存在する場合は、`subdirectory` キーを使って特定のサブディレクトリを指定することができます。

```toml
[tool.poetry.dependencies]
package_name = { git = "https://github.com/username/repo.git", subdirectory = "path/to/package" }
```
