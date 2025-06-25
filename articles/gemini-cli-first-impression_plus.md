---
title: "Gemini CLI 早速試してみた"
emoji: "🌊"
type: "tech" 
topics: ["gemini", "claudecode", "geminicli"]
published: true
---

## Gemini CLI 早速試してみた

2025年6月25日の深夜に、GoogleがGemini CLIを発表しました。

まず最初の印象は、Google版のClaude Codeか？ということです。

Claude Codeはその汎用性から、開発者が皆一斉に使い始めたツールなので、それと同じようなものを天下のGoogleが出してきたら、気になりますよね。
ということで、早速試してみました。

以下で、インストールしてください。

```bash
npm install -g @google/gemini-cli
```

## Gemini CLI の機能

Gemini CLIは、オープンソースのターミナル（コマンドライン）専用のAIエージェントです。
これまでコマンドを一つ一つ打ち込んで行っていた作業を、自然言語での対話によって実行できます。

## Gemini CLI が使えるツール

`/tools`と入力することで、Gemini CLIが利用可能なツールの一覧を表示できます。

![alt text](/images/gemini-cli-first-impression_plus/tools.png)

ファイルの読み書き、シェルコマンドの実行、検索を行うためのツールなど、様々なツールが用意されています。

### 検索ツール

Claude Codeは web検索が弱かったですが、さすが検索の大本命のGoogleといったところでしょうか、しっかりツールとして用意されています。

![alt text](/images/gemini-cli-first-impression_plus/image-3.png)

東京の天気を聞いてみました。

普通に検索ツールが呼ばれていますね。Chromeを開くまでもなくターミナルから離れずに検索できるのはとても便利ですね。
ほしい情報が文字情報だけで充分あれば、ターミナルで完結できます。

これが普及しすぎると、Googleの広告収入が減ってしまうのではないかと心配になりますが、一般向けでないからOKという判断でしょうか？

しかし、検索時にgeminiのAPIの制限に引っかかることがあるようです。
試しに、zennにおける記事内の画像の管理方法についてざっくり質問したところ429が返ってきました。

ブラウザでの検索では上位に出てきてすぐに見つかる情報なのですが。

![alt text](/images/gemini-cli-first-impression_plus/error.png)

429の原因は、[こちらの記事](https://blog.g-gen.co.jp/entry/error-code-429-with-gemini)では以下のように説明されています。

> このエラーは、処理のためのリソースが Google 側で枯渇することを防ぐため、Google によって API 利用が制限されていることを意味しています。Google は随時、物理インフラストラクチャを強化していますが、Gemini API は多くのユーザーに利用されているため、しばしばこのメッセージが表示されることがあります。

Githubには同様のエラーの[issue](https://github.com/google-gemini/gemini-cli/issues?q=is%3Aissue%20state%3Aopen%20429)がいくつか上がっていました。

![alt text](/images/gemini-cli-first-impression_plus/issue.png)

### 基本のコマンド

`/help`でコマンドを確認できます。

![alt text](/images/gemini-cli-first-impression_plus/image-1.png)

いろいろありますが、いくつかピックアップします。

#### 1. ローカルファイルとの連携

`@`を使うことで、ローカルのファイルやディレクトリを直接コンテキストとしてAIに認識させ、それに基づいた操作（要約、修正、変換など）が可能です。

`@`と入力すると、候補となるパスを表示してくれるので、そこから選択できます。

![alt text](/images/gemini-cli-first-impression_plus/image.png)

#### 2. シェルコマンドの実行

`!`を入力すると、シェルコマンドを実行できるシェルモードと、AIと対話モードの切り替えができます。

シェルモードでは、通常のシェルコマンドを入力して実行できます。

![alt text](/images/gemini-cli-first-impression_plus/shell_mode.png)

こちらは通常の対話モードです。

![alt text](/images/gemini-cli-first-impression_plus/normal_mode.png)

色が変わって見やすいですね。

しかし、**シェルモードはステートレスのようです。** そのためシェルモードで `cd` コマンドを実行してディレクトリを移動しても、次のコマンドでは元のディレクトリで実行されます。（実質的に移動できません）
そのため、シェルモードでの操作は一時的な操作に限られるようです。

![alt text](/images/gemini-cli-first-impression_plus/image-2.png)

#### 3. MCP 連携

`/mcp` コマンドを使うことで、MCPの設定ができると思ってましたが、[ドキュメント](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/configuration.md)に飛ばされただけでした。

## Gemini CLIの設定

Gemini CLI 自体は、以下のように設定ファイルを読み込むようで、この中に、MCPサーバーの情報も記述することができるようです。

- ユーザー設定ファイル:
  - 場所: `~/.gemini/settings.json` (ここで ~ はホームディレクトリを指します)
  - スコープ: 現在のユーザーのすべてのGemini CLIセッションに適用されます。

- プロジェクト設定ファイル:
  - 場所: プロジェクトのルートディレクトリ内の `.gemini/settings.json`
  - スコープ: 特定のプロジェクトからGemini CLIを実行する場合にのみ適用されます。プロジェクト設定はユーザー設定を上書きします。

## まとめ

今回は省略しましたが、Gemini CLIで簡単なアプリも作ってみましたが、基本的には Claude Code と同じような使い方ができるので、開発者にとっては使いやすいツールだと思います（Google版のClaude Codeです）。

さらに、現時点で最強の Gemini2.5 Proをバックエンドに持つため、AIの性能も非常に高いです。

そしてweb検索機能もあるため、AIに最新の情報を参照させて開発させるという、Claude Codeでは辛かったこともできるのが嬉しいですね。
