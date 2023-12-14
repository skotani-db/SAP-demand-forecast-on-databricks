---
title: "Amazon AppFlow で SAP データ抽出フローを設定"
weight: 202
---

## 販売伝票ヘッダーのテーブルデータを抽出

1. [Amazon AppFlow のメインコンソールページ](https://us-east-1.console.aws.amazon.com/appflow/home?region=us-east-1#/)で **フローを作成** をクリックします。
    ![AppFlow console](/static/01-data-ingestion/option1-ingest-from-sap/image07.ja.png)
2. **Flow name** で、`salesheader` を入力します。
3. **Customize encryption settings (advanced)**（*暗号化設定をカスタマイズする (高度)*）では、デフォルトのままにして、デフォルトの AWS KMS キーを使用し暗号化ようにします。
4. **次へ** をクリックします。

    ![Flow detail settings](/static/01-data-ingestion/option1-ingest-from-sap/image08.ja.png)
5. **送信元名** に `SAP OData` を選択します。
6. SAP OData 接続を選択のフィールドで、**接続を選択** プルダウンから先ほど作成した接続先 `S4HANACLNT100_Pub` を選択します。
7. 接続先が選択されたら、**SAP OData オブジェクトを選択** のプルダウンで対象の SAP S/4HANA システムのすべての OData サービスが表示されるはずです。一覧から `ZORDER_HEADER_VBAK1` で始まるオブジェクトを選択します。
8. **SAP OData サブオブジェクトを選択** のプルダウンで `EntityOfZVBKATEST` を選択します。
    ![Flow source settings](/static/01-data-ingestion/option1-ingest-from-sap/image09.ja.png)
9. 送信先の詳細で、**送信先名** で Amazon S3 を選択します。
10. **バケットの詳細** で [SAP から抽出したデータを保存するための Amazon S3 バケットを作成](/content/09-end-to-end-workshop/01-data-ingestion/option1-ingest-from-sap/101-preparation.ja.md#sap-から抽出したデータを保存するための-amazon-s3-バケットを作成)で作成したバケット `<AWSAccountID>-appflowodata-<YYYYMMDD>` を選択します。
11. **ファイル形式の設定** で Parquet 形式を選択し、**Parquet 出力でソースのデータ型を保持** にチェックします。

::alert[Parquet 形式を選択する工程は忘れやすいので注意してください]{type=warning}

![File format settings](/static/01-data-ingestion/option1-ingest-from-sap/image10.ja.png)

12. **フロートリガー** で **オンデマンドで実行** を選択し、次へをクリックします。
    ![Flow trigger settings](/static/01-data-ingestion/option1-ingest-from-sap/image11.ja.png)
13. データフィールドをマッピング画面で、マッピング方法を **手動でフィールドをマッピングする** を選択します。
14. **送信元から送信先フィールドへのマッピング** 内の **送信元フィールド名** のプルダウンメニューで **すべてのフィールドを直接マッピングする** を選択します。
    ![data field mapping settings](/static/01-data-ingestion/option1-ingest-from-sap/image12.ja.png)
15. すべてのフィールドが表示されることを確認し、**次へ** をクリックします。
    ![mapped fields](/static/01-data-ingestion/option1-ingest-from-sap/image13.ja.png)
16. **フィルターを追加する** 画面で何も設定しないままで、**次へ** をクリックします。
    ![Add filter](/static/01-data-ingestion/option1-ingest-from-sap/image14.ja.png)
17. 最後の入力確認画面で、入力値を確認し、**フローを作成** ボタンをクリックします。
    ![Create flow button](/static/01-data-ingestion/option1-ingest-from-sap/image15.ja.png)
18. フローが正常に作成されたことを確認します。
19. **フローを実行** ボタンをクリックし、データ抽出フローを実行させます。
    ![execute flow](/static/01-data-ingestion/option1-ingest-from-sap/image16.ja.png)
20. フローが正常に完了し、抽出された件数と格納場所がメッセージに表示されることを確認します。
    ![flow execution succeeded](/static/01-data-ingestion/option1-ingest-from-sap/image17.ja.png)
21. 指定した Amazon S3 バケットにフロー名の Prefix が作成され、その中に今回抽出したファイルが保存されていることを確認します。ダウンロードしたり、Amazon S3 Query でファイル参照することも可能です。
    ![Check ingested objects](/static/01-data-ingestion/option1-ingest-from-sap/image18.ja.png)


## 販売伝票明細のテーブルデータを抽出

ここまでと同様の手順で販売伝票明細のデータを抽出していきます。

1. [Amazon AppFlow のメインコンソールページ](https://us-east-1.console.aws.amazon.com/appflow/home?region=us-east-1#/)で **フローを作成** をクリックします。
2. **Flow name** で、`salesitem` と入力します。
3. **Customize encryption settings (advanced)** (*暗号化設定をカスタマイズする (高度)*) は、デフォルトのままにして、デフォルトの AWS KMS キーを使用して暗号化するようにします。
4. **次へ** をクリックします。
    ![flow detail settings](/static/01-data-ingestion/option1-ingest-from-sap/image19.ja.png)
5. **送信元名** に `SAP OData` を選択します。
6. **SAP OData 接続を選択** のフィールドで、**接続を選択** プルダウンから先ほど作成した接続先 `S4HANACLNT100_Pub` を選択します。
7. 接続先が選択されたら、**SAP OData オブジェクトを選択** のプルダウンで対象の SAP S/4HANA システムのすべての OData サービスが表示されるはずです。一覧から `ZORDER_ITEM_VBAP` から始まるオブジェクトを選択します。
8. **SAP OData サブオブジェクトを選択** のプルダウンで `EntityOfZVBAPTEST` を選択します。
    ![flow source settings](/static/01-data-ingestion/option1-ingest-from-sap/image20.ja.png)
9. **送信先の詳細** の、**送信先名** で Amazon S3 を選択します。
10. **バケットの詳細** で [SAP から抽出したデータを保存するための Amazon S3 バケットを作成](/content/09-end-to-end-workshop/01-data-ingestion/option1-ingest-from-sap/101-preparation.ja.md#sap-から抽出したデータを保存するための-amazon-s3-バケットを作成) のセクションで作成したバケット `<AWSAccountID>-appflowodata-<YYYYMMDD>` を選択します。
11. **ファイル形式の設定** で Parquet 形式を選択し、**Parquet 出力でソースのデータ型を保持** にチェックします。

::alert[Parquet 形式を選択する工程は忘れやすいので注意してください]{type=warning}

![flow target settings](/static/01-data-ingestion/option1-ingest-from-sap/image21.ja.png)
12. **フロートリガー** で **オンデマンドで実行** を選択し、**次へ** をクリックします。
    ![flow trigger settings](/static/01-data-ingestion/option1-ingest-from-sap/image22.ja.png)
13. データフィールドをマッピング画面で、マッピング方法を **「手動でフィールドをマッピングする」** を選択します。
14. **送信元から送信先フィールドへのマッピング** の中の **送信元フィールド名** のプルダウンメニューで **すべてのフィールドを直接マッピングする** を選択します。
    ![data field mapping](/static/01-data-ingestion/option1-ingest-from-sap/image23.ja.png)
15. すべてのフィールドが表示されることを確認し、**次へ** をクリックします。
    ![mapped fields](/static/01-data-ingestion/option1-ingest-from-sap/image24.ja.png)
16. **フィルターを追加する** 画面で何も設定しないままで、 **次へ** をクリックします。
    ![add filter](/static/01-data-ingestion/option1-ingest-from-sap/image25.ja.png)
17. 最後の入力確認画面で、入力値を確認し、**フローを作成** ボタンをクリックします。
    ![create flow button](/static/01-data-ingestion/option1-ingest-from-sap/image26.ja.png)
18. フローが正常に作成されたことを確認します。
19. **フローを実行** ボタンをクリックし、データ抽出フローを実行させます。
    ![execute flow](/static/01-data-ingestion/option1-ingest-from-sap/image27.ja.png)
20. フローが正常に完了し、抽出された件数と格納場所がメッセージに表示されることを確認します。
    ![flow execution message](/static/01-data-ingestion/option1-ingest-from-sap/image28.ja.png)
21. 指定した Amazon S3 バケットにフロー名の Prefix が作成され、その中に今回抽出したファイルが保存されることを確認します。ダウンロードしたり、Amazon S3 Query でファイル参照することも可能です。
    ![ingested objects](/static/01-data-ingestion/option1-ingest-from-sap/image29.ja.png)
