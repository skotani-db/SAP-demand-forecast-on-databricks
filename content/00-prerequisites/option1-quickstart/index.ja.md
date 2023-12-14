---
title: "2. (Option 1) クイックスタート"
weight: 12
---

::alert[本ワークショップを実行するには Databricks の管理者アカウントおよび AWS アカウントの管理者権限が必要です。Databricks の管理者アカウントをお持ちでない場合は[こちら](https://www.databricks.com/try-databricks-aws#account)から無料トライアルを開始してください。]{type=warning}

## Databricks 無料トライアルアカウントの作成

[こちら](https://www.databricks.com/try-databricks-aws#account) から Databricks の無料トライアルアカウントを作成していきます。

1. フォームに必要な情報を記入し、「Continue」ボタンをクリックしてください。

![Create your account](/static/00-prerequisites/create-your-account.png)

2. 料金の支払い方法は「Pay with credit card」を選択し、「Continue」ボタンをクリックしてください。

::alert[なお、14日間の無料トライアル中はクレジットカード情報を入力しなくても使えます。また、トライアルが終了してもクレジットカード情報を入力してプラン継続しない限り課金されないので安心してください。]{type=info}
![Pay with credit card](/static/00-prerequisites/pay-with-credit-card.png)

3. 入力したメールアドレスに以下のようなメールが届きます。「Verify email address now」ボタンをクリックします。

![Verify your email address](/static/00-prerequisites/verify-email-address-now.png)

4. 好きなパスワードを入力してください。このパスワードはあとの工程でも複数回使うので忘れずにメモしておいてください。

![Set your password](/static/00-prerequisites/set-your-password.png)

::alert[次の工程は [1. AWS ハンズオンアカウントへのログイン](/00-prerequisites/workshop-studio) の手順からハンズオン用の AWS 環境にログインした上で実行してください。]{type=warning}

5. ワークスペース名には `workshop`、AWS リージョンはバージニア北部 `N.Virginia (us-east-1)` を選択して「Start quickstart」ボタンをクリックしてください。

![Setup your first workspace](/static/00-prerequisites/setup-your-first-workspace.png)

6. AWS CloudFormation のスタックを作成する画面に遷移します。パラメーターのうち `Databricks account password` に先ほど設定したパスワードを入力し、ページ下部の「I acknowledge that AWS CloudFormation might create IAM resources with custom names.」のチェックボックスを入れ、「Create stack」ボタンをクリックします。

![Create databricks quickstart stack](/static/00-prerequisites/create-databricks-quickstart-stack.png)

これで自動的にワークスペースのプロビジョニングが始まります。
通常、プロビジョニングは5分程度でます。

メールでワークスペースの URL が届くのでアクセスし、ログインしてください。
ログイン名およびパスワードは管理コンソールにログインするときのものと同じです。

### コラム: Databricks ワークスペースのデプロイ

Databricks のワークスペースをデプロイする方法は2つあります。

ひとつはマニュアルで皆様の AWS アカウントと Databricks の所有するアカウントとを繋ぐクロスアカウントロール、およびルートストレージ用の S3 バケットを用意し、オプションとしてお客様管理の VPC や PrivateLink の設定をし、デプロイする方法です。
本番環境のワークスペースのデプロイはこちらの方法が推奨されます。

もうひとつの方法として、今回のようなワークショップで使用する環境は Quickstart オプション (AWS CloudFormation テンプレートを利用) が推奨されます。
AWS リソースが自動的に作成・設定されるため、ワークスペースを作成する方法として簡易的です。
また Unity Catalog というデータカタログが自動で設定されるため、 Databricks におけるデータガバナンス機能をすぐに試すことができます。

本ラボでは、 Databricks ワークスペースを Quickstart オプションでデプロイします。

::alert[Quickstart では、すでにお使いの Databricks アカウントで Unity Catalog を設定していて同一リージョンにメタストアが存在する場合、自動的にワークスペースへメタストアがアタッチされます。]{type=info}

<!--
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
通常、プロビジョニングは5分程度でます。

メールでワークスペースの URL が届くのでアクセスし、ログインしてください。
ログイン名およびパスワードは管理コンソールにログインするときのものと同じです。
-->
