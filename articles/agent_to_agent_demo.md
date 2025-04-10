---
title: "A2A(Agent2Agent Protocol)デモを試す"
emoji: "🤖"
type: "tech" # tech: 技術記事 / idea: アイデア
topics: ["aiエージェント", "A2A", "Agent2Agent"]
published: false
---

## Agent2Agent (A2A)とは

2025年4月9日にGoogleからAgent2Agent Protocol (A2A)が[発表](https://developers.googleblog.com/en/a2a-a-new-era-of-agent-interoperability/)されました。これはAIエージェント間の通信のためのプロトコルです。

GoogleCloudの[ブログ](https://cloud.google.com/blog/ja/products/ai-machine-learning/a2a-a-new-era-of-agent-interoperability)には以下のようにも記載されており、今後エージェント間の相互運用におけるデファクトスタンダードになることが期待されています。

>この取り組みには、Atlassian、Box、Cohere、Intuit、Langchain、MongoDB、PayPal、Salesforce、SAP、ServiceNow、UKG、Workday など 50 以上のテクノロジーパートナーと Accenture、BCG、Capgemini、Cognizant、Deloitte、HCLTech、Infosys、KPMG、McKinsey、PwC、TCS、Wipro といった主要なサービス プロバイダーが参加しています。
>この共同の取り組みは、基盤技術に関わらず、AI エージェントがシームレスに連携し、複雑な企業ワークフローを自動化して、これまでにない効率性と革新をもたらす未来へのビジョンを示しています。

## デモ

解説は公式がわかりやすいのでそちらをみていただくとして、今回は公開されているデモを通してA2Aを理解していきたいと思います。

リポジトリ: [https://github.com/google/A2A](https://github.com/google/A2A)

### デモアプリの全体像

詳細はリポジトリに記載されているので割愛しますが、デモアプリは1つのホストエージェントを持ち、3つのリモートのエージェントA2Aを用いて連携できるものになっています。

A2Aはエージェントの実装に関わらず、アージェント同志の連携を可能にするプロトコルです。デモアプリで使用する3つのリモートエージェントも以下の3つ異なるフレームワークで実装されています。

- CrewAI
- Google ADK
- LangGraph

![demo-app](https://github.com/Nao-Y1996/zenn-content/blob/main/articles/images/a2a-demo/demo-app.png?raw=true)

### エージェントの登録

デモアプリと3つのエージェントのA2Aサーバーを立ち上げます（やり方はリポジトリにあるので割愛）

アプリではIPアドレスを指定してリモートエージェントをできる画面があります。

![add_agent](https://github.com/Nao-Y1996/zenn-content/blob/main/articles/images/a2a-demo/add_agent.png?raw=true)

CrewAIのエージェントは `localhost:8080`で起動したのでそれを入れてみます。

以下のような情報が表示されました。

![add-crewai-agent](https://github.com/Nao-Y1996/zenn-content/blob/main/articles/images/a2a-demo/add-crewai-agent.png?raw=true)

A2Aをサポートするリモートエージェントは、エージェントの能力/スキルと認証メカニズムを記述したAgent Card をJSON形式で公開する必要があります。ここでは、AgentCardの情報が表示されているようです。

Agent Card は <https://base-url/.well-known/agent.json> にホストすることが[推奨されており](https://google.github.io/A2A/#/documentation?id=discovery)、試しにブラウザで直接 `localhost:8080/.well-known/agent.json`にアクセスしてみると、画面で表示されたものと同様の以下のようなJSONが表示されました。

```json
{
  "name": "Image Generator Agent",
  "description": "Generate stunning, high-quality images on demand and leverage powerful editing capabilities to modify, enhance, or completely transform visuals.",
  "url": "http://0.0.0.0:8080/",
  "version": "1.0.0",
  "capabilities": {
    "streaming": false,
    "pushNotifications": false,
    "stateTransitionHistory": false
  },
  "defaultInputModes": [
    "text",
    "text/plain",
    "image/png"
  ],
  "defaultOutputModes": [
    "text",
    "text/plain",
    "image/png"
  ],
  "skills": [
    {
      "id": "image_generator",
      "name": "Image Generator",
      "description": "Generate stunning, high-quality images on demand and leverage powerful editing capabilities to modify, enhance, or completely transform visuals.",
      "tags": [
        "generate image",
        "edit image"
      ],
      "examples": [
        "Generate a photorealistic image of raspberry lemonade"
      ]
    }
  ]
}
```

クライアントは <https://base-url/.well-known/agent.json> で用意してあるエージェント見にいけるようです。

---

同じように3つのエージェントを登録しました。ちなみに、上から順に

- CrewAI Agent
- Google ADK Agent
- LangGraph Agent

となっています。

![agents](https://github.com/Nao-Y1996/zenn-content/blob/main/articles/images/a2a-demo/agents.png?raw=true)

### チャット

デモアプリのチャット画面で何ができるか聞いてみました（1回目に聞いたときはリモートエージェントを登録する前です）。

![shat-host-agent](https://github.com/Nao-Y1996/zenn-content/blob/main/articles/images/a2a-demo/chat-host-agent.png?raw=true)

画像生成を試しました（geminiで生成されるだけです）。プールの上を走る犬の画像が生成されました。

![generated1](https://github.com/Nao-Y1996/zenn-content/blob/main/articles/images/a2a-demo/generated_1.png?raw=true)

### イベントリスト

チャットで発生したイベントの履歴も取得できているようです。
下から2番目のイベントを見ると画像生成のタスクがImage Ggenerator Agentに渡されていることがわかります。
（Actorがhost_agentになっているのは気になりますが）

![event-list](https://github.com/Nao-Y1996/zenn-content/blob/main/articles/images/a2a-demo/event-list.png?raw=true)
