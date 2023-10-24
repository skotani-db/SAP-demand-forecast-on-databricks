---
title: "Amazon QuickSight を用いた Delta Lake Table の可視化"
weight: 52
---

[Amazon QuickSight](https://aws.amazon.com/quicksight/) は非常に高速で使いやすいクラウド対応のビジネス分析サービスであり、組織内のすべての従業員が可視化の構築、アドホック分析の実行およびデータから、いつでも、どのデバイス上でもビジネスインサイトを迅速に得ることを容易にします。
データソースとしては、Amazon Redshift、Amazon RDS、Amazon Aurora、Amazon Athena、Amazon S3 などの AWS データソースと接続できるだけでなく、CSV および Excel ファイルを直接アップロードしたり、**Databricks** や Salesforce などの SaaS アプリケーションに接続したり、SQL サーバー、MySQL、PostgreSQL などのオンプレミスデータベースにアクセスすることもできます。
QuickSight は優れたインメモリエンジン (SPICE) を使って、組織がそのビジネス分析機能を何十万ものユーザーにスケールし、高速で応答性の良いクエリパフォーマンスを達成できるようにします。

このハンズオンラボでは Databricks の Delta Lake Table に接続し、Databricks 上のデータを QuickSight で可視化する手順を解説します。
最終的な画面イメージはこちらです。

![Final dashboard](/static/04-dashboarding/option2-amazon-quicksight/sales-dashboard.png)

1. 初めに、AWS コンソールにログインしてください。
2. AWS コンソール上部の検索バーに「QuickSight」と入力し、表示された QuickSight のリンクをクリックします。
![Open QuickSight](/static/04-dashboarding/option2-amazon-quicksight/aws-console-search-bar.png)

## 事前準備: QuickSight のセットアップ

QuickSight を初めて利用する場合はまず初期設定を行います。
初期設定済みの場合は次のセクションに進んでください。

::::expand{header="QuickSight のセットアップ手順はこちら" defaultExpanded=false}

1. 「Sign up for QuickSight」ボタンをクリックします。
![Sign up for QuickSight](/static/04-dashboarding/option2-amazon-quicksight/sign-up-for-quicksight.png)
2. 「Enterprise」エディションを選択し、「Continue」ボタンをクリックします。
![Select Enterprise Edition](/static/04-dashboarding/option2-amazon-quicksight/create-your-quicksight-account.png)
3. Paginated Report add-on は今回必要ないので「No, Maybe Later」ボタンをクリックします。
![Paginated Report add-on](/static/04-dashboarding/option2-amazon-quicksight/get-paginated-report-add-on.png)
4. 「Select a region」のボックスではワークショップを実施しているリージョンを選択し、「QuickSight account name」には任意の名前 (`databricks-on-aws-workshop-<your name>` など、一意である必要があります) を入力し、「Notification email address」にはあなたのメールアドレスを入力してください。その他はデフォルトの設定のままにし、「Finish」ボタンをクリックします。
![Additional settings](/static/04-dashboarding/option2-amazon-quicksight/account-setting.png)
5. 初期設定が完了したら「Go to Amazon QuickSight」ボタンをクリックします。

::::

::alert[QuickSight に関連する不要な課金を防ぐため、ワークショップ終了後は [あと片付け](/09-cleanup) の手順で環境を削除してください。]{type=warning}

## QuickSight の Databricks コネクターをセットアップ

QuickSight には [Databricks 用のコネクター](https://aws.amazon.com/about-aws/whats-new/2022/11/amazon-quicksight-supports-connectivity-databricks/)があるので、複雑な設定を行うことなく、Databricks 上のテーブルに接続して QuickSight 上で可視化することができます。

1. 左ペインの「Datasets」をクリックします。
![Select Datasets](/static/04-dashboarding/option2-amazon-quicksight/quicksight-analyses.png)
2. 右上の「New Dataset」ボタンをクリックします。
![Select new dataset](/static/04-dashboarding/option2-amazon-quicksight/quicksight-datasets.png)
3. データソースのリストから「Databricks」を探し、クリックします。
![Select Databricks](/static/04-dashboarding/option2-amazon-quicksight/quicksight-connectors.png)

接続先の情報を入力するモーダルウィンドウが表示されます。
次の手順で Databricks クラスターへの JDBC 接続情報を確認し、入力していきます。

### Databricks クラスターへの JDBC 接続情報を確認

::alert[クラスターが起動状態であることを確認してください。停止している場合は QuickSight から接続できません。]{type=warning}

1. Databricks のワークスペースを開きます。
2. 左ペインの「Compute」をクリックし、クラスターのリストを開きます。
![Select Compute](/static/04-dashboarding/option2-amazon-quicksight/databricks-main.png)
3. 前回までのラボで用いていたクラスターの名前をクリックします。
4. 下部の「Advanced options」メニューを開き、「JDBC/ODBC」タブをクリックします。

ここで表示されている項目を QuickSight に入力していきます。

### QuickSight の Databricks コネクターを作成

QuickSight の画面に戻ります。

1. 「Data source name」欄には任意の名前 (例: `Databricks on AWS Workshop`)、「Database server」欄には「Server Hostname」の値 (例: `foo.cloud.databricks.com`)、「HTTP Path」欄には「HTTP Path」の値、「Port」欄には `443`、「Username」および「Password」欄にはワークスペースログイン時のユーザー名とパスワードを入力してください。
![New databricks data source](/static/04-dashboarding/option2-amazon-quicksight/new-databricks-data-source.png)
2. 「Validate connection」をクリックして問題がなければ「Create data source」ボタンをクリックしてください。
3. 「Choose your table」の画面の「Catalog: contain sets of schemas.」では `hive_metastore` を選択し、「Schema: contain sets of tables.」は `default` を選択してください。
4. 「Tables: contain the data you can visualize.」にテーブルのリストが表示されます。`sales_forecast` を選択し、「Select」ボタンをクリックしてください。
![Choose your table](/static/04-dashboarding/option2-amazon-quicksight/choose-your-table.png)
5. 「Finish dataset creation」の画面では変更せずそのまま「Visualize」ボタンをクリックします。ダッシュボードの編集画面が開きます。
![finish dataset creation](/static/04-dashboarding/option2-amazon-quicksight/finish-dataset-creation.png)

画面左上の QuickSight のロゴをクリックし、QuickSight のホーム画面を開いてください。
再度、Datasets → New dataset と遷移し、データセット追加の画面に移動します。

先ほどは機械学習の売上予測と実績値を含んだ `sales_forecast` テーブルをインポートしましたが、もうひとつテーブル `sales_record_silver` をインポートします。

6. ページ下部の「FROM EXISTING DATA SOURCES」にある、先ほど作成したデータソース (例: `Databricks on AWS Workshop`) をクリックします.

![select data source](/static/04-dashboarding/option2-amazon-quicksight/from-existing-data-sources.png)

7. 「Create dataset」ボタンをクリックします。
8. 先ほどと同様に、「Choose your table」の画面の「Catalog: contain sets of schemas.」では `hive_metastore` を選択し、「Schema: contain sets of tables.」は `default` を選択してください。
9. 「Tables: contain the data you can visualize.」にテーブルのリストが表示されます。`sales_record_silver` を選択し、「Select」ボタンをクリックしてください。
10. 「Finish dataset creation」の画面では変更せずそのまま「Visualize」ボタンをクリックします。ダッシュボードの編集画面が開きます。

## Amazon QuickSight でダッシュボードを作成

開いたダッシュボード編集画面で作業します。

::alert[閉じてしまった場合は「Quick Sight のトップページ」→「Analyses」→「sales_record_silver analysis」を開いてください。]{type=info}

New sheet というタイトルのモーダルが表示されていたら Interactive sheet を選択して「Create」をクリックしてください。

まず、可視化で使うテーブルをダッシュボードに追加します。

1. ダッシュボードの「Visualize」アイコンの右にある鉛筆マークをクリックします。

![](/static/04-dashboarding/option2-amazon-quicksight/add-dataset.png)

2. 「Add dataset」をクリックします。
3. 「sales_forecast」を選択し、「Select」ボタンをクリックします。

sales_forecast と sales_record_silver のデータセットが読み込めていれば準備完了です。

![datasets in this analysis](/static/04-dashboarding/option2-amazon-quicksight/datasets-in-this-analysis.png)

以下のスクリーンショットを参考に可視化してみましょう。

1. 左上の Dataset は sales_record_silver を選択し、ItemGroup と Price のフィールドを選択し、左下の Visual types から Clustered bar combo chart を選択してください。
2. 上部の Field wells では X axis に ItemGroup、Bars に Price、Lines に ItemGroup を選択します。
3. グラフ横軸のラベル (Group By: ItemGroup) の左にある矢印アイコンをクリックするとソート順を変えられます。
4. グラフ右上の鉛筆アイコンをクリックし、左ペインの Data labels メニューを開き、Bars と Lines に対して Show data labels のボックスにチェックを入れるとデータポイントの付近に数値ラベルが追加されます。

![sales and sales volume results by product category](/static/04-dashboarding/option2-amazon-quicksight/sales-and-sales-volume-results-by-product-category.png)

追加のグラフを作成するには画面左上の「＋ ADD」をクリックし、Add visual をクリックします。
以下のスクリーンショットを参考に可視化してみましょう。

1. 左上の Dataset は sales_forecast を選択し、Price と Price_lower と Price_upper と YearMonth のフィールドを選択し、左下の Visual types から Line chart を選択してください。
2. 上部の Field wells では X asis に YearMonth、Value に Price、Price_upper、Price_lower を選択します。
3. グラフ内のデータポイントをクリックし、Style all series... をクリックし、Marker をオンにすると各データポイントに丸点が表示されます。

![actual and forecasted overall sales](/static/04-dashboarding/option2-amazon-quicksight/actual-and-forecasted-overall-sales.png)

最終的なダッシュボードは以下のようになります。

![Final dashboard](/static/04-dashboarding/option2-amazon-quicksight/sales-dashboard.png)
## 参考文献

- [Using Databricks in QuickSight](https://docs.aws.amazon.com/quicksight/latest/user/quicksight-databricks.html)
- [Amazon QuickSight Administrator's guide to connecting Databricks](https://docs.aws.amazon.com/quicksight/latest/user/quicksight-databricks-administration-setup.html)
- [Configure the Databricks ODBC and JDBC drivers](https://docs.databricks.com/integrations/jdbc-odbc-bi.html#get-server-hostname-port-http-path-and-jdbc-url)
