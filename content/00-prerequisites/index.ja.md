---
title: "事前準備: Databricks on AWS のセットアップ"
weight: 10
---

事前準備として Databricks on AWS のセットアップを行います。

## Databricks ワークスペースの作成

Databricks on AWS の SaaS プラットフォームは2つ (以上) のアカウントで構成されます。
ひとつは Databricks が所有する AWS アカウント内にコントロールプレーンが作成され、ウェブアプリケーションの UI の提供やノートブックやその他メタデータはこちらで管理されます。
一方、データ処理を行う Spark クラスターや S3 上のデータセットはデータプレーンとしてユーザーの AWS アカウント内に存在することになります。
![Databricks Architecture](/static/00-prerequisites/databricks-architecture.png)

以下のリンクから、皆さまの AWS アカウントの上で稼働する Databricks ワークスペースを作成する手順を確認してください。

::children
