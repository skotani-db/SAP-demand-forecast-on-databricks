---
title: "Amazon AppFlowで SAP データ抽出フローを設定"
weight: 202
---

## 販売伝票ヘッダーのテーブルデータを抽出

1. [Amazon AppFlow のメインコンソールページ](https://us-east-1.console.aws.amazon.com/appflow/home?region=us-east-1#/)で **フローを作成** をクリックします。
    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image07.ja.png)
1. **Flow name** で、`salesheader` を入力します。
1. **Customize encryption settings (advanced)**（*暗号化設定をカスタマイズする (高度)*）では、デフォルトのままにして、デフォルトの AWS KMS キーを使用し暗号化ようにします。
1. **次へ** をクリックします。

    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image08.ja.png)
1. **送信元名** に `SAP OData` を選択します。
1. SAP OData接続を選択のフィールドで、**接続を選択**プルダウンから先ほど作成した接続先`S4HANACLNT100_Pub`を選択します。
1. 接続先が選択されたら、**SAP OData オブジェクトを選択**のプルダウンで対象のSAP S/4HANAシステムのすべてのODataサービスが表示されるはずです。一覧から`ZORDER_HEADER_VBAK1`から始まりのオブジェクトを選択します。
1. **SAP OData サブオブジェクトを選択**のプルダウンで`EntityOfZVBKATEST`を選択します。
    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image09.ja.png)
1. 送信先の詳細で、**送信先名**でAmazon S3を選択します。
1. **バケットの詳細**で[SAP から抽出したデータを保存するための Amazon S3 バケットを作成](/content/09-end-to-end-workshop/01-data-ingestion/option1-ingest-from-sap/101-preparation.ja.md#sap-から抽出したデータを保存するための-amazon-s3-バケットを作成)で作成したバケット`<AWSAccountID>-appflowodata-<MMDD>`を選択します。
1. **ファイル形式の設定**でParquet形式を選択し、Parquet出力でソースのデータ型を保持にチェックします。
    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image10.ja.png)
1. **フロートリガー**で**オンデマンドで実行**を選択し、次へをクリックします。
    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image11.ja.png)
1. データフィールドをマッピング画面で、マッピング方法を**手動でフィールドをマッピングする**を選択します。
1. **送信元から送信先フィールドへのマッピング**で**送信元フィールド名**を**すべてのフィールドを直接マッピングする**を選択します。
    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image12.ja.png)
1. 全てのフィールドが表示されることを確認し、**次へ**をクリックします。
    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image13.ja.png)
1. **フィルターを追加する**画面で何も設定しないままで、**次へ**をクリックします。
    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image14.ja.png)
1. 最後の入力確認画面で、入力値を確認し、**フローを作成**ボタンをクリックします。

    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image15.ja.png)
1. フローが正常に作成されたことを確認します。
2. **フローを実行**ボタンをクリックし、データ抽出フローを実行させます。
    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image16.ja.png)
1. フローが正常に完了し、抽出された件数と格納場所がメッセージに表示されることを確認します。
    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image17.ja.png)
1. 指定したAmazon S3バケットにフロー名のPrefixが作成され、その中に今回抽出したファイルが保存されることを確認します。ダウンロードしたり、Amazon S3 Queryでファイル参照することも可能です。
    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image18.ja.png)


## 販売伝票明細のテーブルデータを抽出
1. [Amazon AppFlow のメインコンソールページ](https://us-east-1.console.aws.amazon.com/appflow/home?region=us-east-1#/)で **フローを作成** をクリックします。
1. **Flow name** で、`salesitem` を入力します。
1. **Customize encryption settings (advanced)**（*暗号化設定をカスタマイズする (高度)*）では、デフォルトのままにして、デフォルトの AWS KMS キーを使用し暗号化ようにします。
1. **次へ** をクリックします。

    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image19.ja.png)
1. **送信元名** に `SAP OData` を選択します。
1. SAP OData接続を選択のフィールドで、**接続を選択**プルダウンから先ほど作成した接続先`S4HANACLNT100_Pub`を選択します。
1. 接続先が選択されたら、**SAP OData オブジェクトを選択**のプルダウンで対象のSAP S/4HANAシステムのすべてのODataサービスが表示されるはずです。一覧から`ZORDER_ITEM_VBAP`から始まりのオブジェクトを選択します。
1. **SAP OData サブオブジェクトを選択**のプルダウンで`EntityOfZVBAPTEST`を選択します。
    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image20.ja.png)
1. 送信先の詳細で、**送信先名**でAmazon S3を選択します。
1. **バケットの詳細**で[SAP から抽出したデータを保存するための Amazon S3 バケットを作成](/content/09-end-to-end-workshop/01-data-ingestion/option1-ingest-from-sap/101-preparation.ja.md#sap-から抽出したデータを保存するための-amazon-s3-バケットを作成)で作成したバケット`<AWSAccountID>-appflowodata-<MMDD>`を選択します。
1. **ファイル形式の設定**でParquet形式を選択し、Parquet出力でソースのデータ型を保持にチェックします。
    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image21.ja.png)
1. **フロートリガー**で**オンデマンドで実行**を選択し、次へをクリックします。
    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image22.ja.png)
1. データフィールドをマッピング画面で、マッピング方法を **「手動でフィールドをマッピングする」** を選択します。
1. **送信元から送信先フィールドへのマッピング**で**送信元フィールド名**を**すべてのフィールドを直接マッピングする**を選択します。
    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image23.ja.png)
1. 全てのフィールドが表示されることを確認し、**次へ**をクリックします。
    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image25.ja.png)
1. **フィルターを追加する** 画面で何も設定しないままで、 **次へ** をクリックします。
    
    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image26.ja.png)
1. 最後の入力確認画面で、入力値を確認し、**フローを作成** ボタンをクリックします。
    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image27.ja.png)
1. フローが正常に作成されたことを確認します。
1. **フローを実行** ボタンをクリックし、データ抽出フローを実行させます。
1. フローが正常に完了し、抽出された件数と格納場所がメッセージに表示されることを確認します。
    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image28.ja.png)
1. 指定したAmazon S3バケットにフロー名のPrefixが作成され、その中に今回抽出したファイルが保存されることを確認します。ダウンロードしたり、Amazon S3 Queryでファイル参照することも可能です。
    ![pic](/static/01-data-ingestion/option1-ingest-from-sap/image29.ja.png)
