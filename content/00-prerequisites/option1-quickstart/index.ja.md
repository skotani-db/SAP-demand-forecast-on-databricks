---
title: "Option 1: クイックスタート"
weight: 11
---

::alert[本ワークショップを実行するには Databricks の管理者アカウントおよび AWS アカウントの管理者権限が必要です。Databricks の管理者アカウントをお持ちでない場合は[こちら](https://www.databricks.com/try-databricks-aws#account)から無料トライアルを開始してください。]{type=warning}

### Databricks ワークスペースをクイックスタートオプションでデプロイする

Databricks のワークスペースをデプロイする方法は2つあります。

ひとつはマニュアルで皆様の AWS アカウントと Databricks の所有するアカウントとを繋ぐクロスアカウントロール、およびルートストレージ用の S3 バケットを用意し、オプションとしてお客様管理の VPC や PrivateLink の設定をし、デプロイする方法です。
本番環境のワークスペースのデプロイはこちらの方法が推奨されます。

もうひとつの方法として、今回のようなワークショップで使用する環境は Quickstart オプション ( CloudFormation テンプレートを利用) が推奨されます。
AWS リソースが自動的に作成・設定されるため、ワークスペースを作成する方法として簡易的です。
また Unity Catalog というデータカタログが自動で設定されるため、 Databricks におけるデータガバナンス機能をすぐに試すことができます。

本ラボでは、 Databricks ワークスペースを Quickstart オプションでデプロイします。

::alert[Quickstart では、すでにお使いの Databricks アカウントで Unity Catalog を設定していて同一リージョンにメタストアが存在する場合、自動的にワークスペースへメタストアがアタッチされます。]{type=warning}

1. [AWS のマネジメントコンソール](https://aws.amazon.com/jp/console/)にアクセスします。

2. 別タブで [Databricks の管理者コンソール](https://accounts.cloud.databricks.com/)にアクセスし、左ペインの 「Workspaces」 をクリックしてください。

![Select Workspaces tab](/static/00-prerequisites/select-workspaces-tab.png)

3. 右上の Create workspace をクリックして、 「Quickstart」 オプションを選択して、 「Next」 をクリックします。

![QuickStart Option](/static/00-prerequisites/select-quickstart.png)

4. 「Workspace name」に `workshop` を入力し、 「Region」には `N.Virginia (us-east-1)` を選択し、「Start Quickstart」をクリックします。

![Workspace Information](/static/00-prerequisites/workspace-info.png)

5. AWS コンソール側で Databricks ワークスペースを構成するために必要なリソースを定義する CloudFormation スタックが立ち上がります。Databricks 管理アカウントのパスワードを入力し、IAM リソースが自動で作成されることに同意するチェックボックスを押して、「スタックを作成」をクリックすると、ワークスペースのデプロイが開始されます。

![CFn Stack](/static/00-prerequisites/create-workspace-quickstart.png)

これで自動的にワークスペースのプロビジョニングが始まります。
ワークスペースのリストからステータスを確認し、Provisioning から Running に変われば準備完了です。 
通常、プロビジョニングは5分程度で完了します。

メールでワークスペースの URL が届くのでアクセスし、ログインしてください。
ログイン名およびパスワードは管理コンソールにログインするときのものと同じです。
