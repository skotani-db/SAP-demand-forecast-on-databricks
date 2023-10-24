---
title: "事前準備：S3 バケットの作成と SAP Odata コネクタ接続先の設定"
weight: 201
---

## SAP から抽出したデータを保存するための Amazon S3 バケットを作成

1. [Amazon S3 コンソール](https://s3.console.aws.amazon.com/s3/home)を開きます。
1. **バケットを作成** をクリックします。
1. バケットを作成したい **AWS リージョン** を選択します。 (基本的には us-east-1 に設定)
1. バケット名を `<AWSAccountID>-appflowodata-<YYYYMMDD>` に設定します。バケット名はユニークである必要があります。自分の AWS アカウント ID `<AWSAccountID>` は AWS マネージメントコンソールの右上で確認できますが、アカウント ID 番号に入っている「-」は削除するようにご注意ください。
1. 他の値はデフォルト値のままにし、画面の一番下にスクロールし、**バケットを作成** をクリックします。 選択したリージョンで S3 バケットが作成されます。

![create bucket](/static/01-data-ingestion/option1-ingest-from-sap/image01.en.png)
![create bucket - additional settings](/static/01-data-ingestion/option1-ingest-from-sap/image02.en.png)

## AppFlow で、SAP の接続先 ( Connection ) を設定

1. [Amazon AppFlow のメインコンソールページ](https://us-east-1.console.aws.amazon.com/appflow/home?region=us-east-1#/)を開き、左メニューを開き、[接続画面](https://us-east-1.console.aws.amazon.com/appflow/home?region=us-east-1#/connections)を開きます。
1. **コネクタのドロップダウン** から **SAP OData** を選択します。
    ![Select SAP Odata](/static/01-data-ingestion/option1-ingest-from-sap/image03.ja.png)
1. **接続を作成** ボタンをクリックします。
*フロー作成画面でも接続先の作成ができますが、そこで接続エラーが発生するとフロー名の再入力手間が発生するため、独立ステップとして実施します。*
    ![Create Connection](/static/01-data-ingestion/option1-ingest-from-sap/image04.ja.png)
1. SAP Odata に接続のポップアップに以下の接続情報を入力し、**接続する** ボタンをクリックし、接続先を作成します。
    |項目	|値	|
    |---	|---	|
    |接続名	|S4HANACLNT100_Pub	|
    |認証モードを選択	|ベーシック認証	|
    |ユーザー名	|講師が指定した SAP ユーザー	|
    |パスワード	|講師が指定した SAP ユーザーのパスワード	|
    |アプリケーションのホスト URL	|講師が指定した URL (例：http://hostname.aws.dev)	※ |
    |アプリケーションサービスへのパス	|/sap/opu/odata/iwfnd/catalogservice;v=2	|
    |ポート番号	|443	|
    |クライアント番号	|100	|
    |ログオンする言語	|EN	|
    |PrivateLink	|無効	|
    |データ暗号化	|選択しない	|
    |	|	|

    ::alert[**※アプリケーションホストURLの末尾に「/」を記載しないでください。接続エラーになります。**]{type=warning}

    ![Connection to SAP OData](/static/01-data-ingestion/option1-ingest-from-sap/image05.en.png)
1. 接続先が正常に作成されたことを確認します。
    ![Connection is successfully created](/static/01-data-ingestion/option1-ingest-from-sap/image06.ja.png)
