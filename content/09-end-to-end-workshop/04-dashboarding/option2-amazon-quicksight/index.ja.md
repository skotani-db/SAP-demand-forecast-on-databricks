---
title: "Amazon QuickSight を用いた Delta Lake Table の可視化"
weight: 52
---

[Amazon QuickSight](https://aws.amazon.com/quicksight/) は非常に高速で使いやすいクラウド対応のビジネス分析サービスであり、組織内のすべての従業員が可視化の構築、アドホック分析の実行およびデータから、いつでも、どのデバイス上でもビジネスインサイトを迅速に得ることを容易にします。
データソースとしては、Amazon Redshift、Amazon RDS、Amazon Aurora、Amazon Athena、Amazon S3 などの AWS データソースと接続できるだけでなく、CSV および Excel ファイルを直接アップロードしたり、**Databricks** や Salesforce などの SaaS アプリケーションに接続したり、SQL サーバー、MySQL、PostgreSQL などのオンプレミスデータベースにアクセスすることもできます。
QuickSight は優れたインメモリエンジン (SPICE) を使って、組織がそのビジネス分析機能を何十万ものユーザーにスケールし、高速で応答性の良いクエリパフォーマンスを達成できるようにします。

このハンズオンラボでは Databricks の Delta Lake Table に接続し、Databricks 上のデータを QuickSight で可視化する手順を解説します。

## 事前準備: Amazon QuickSight のセットアップ

QuickSight を初めて利用する場合はまず初期設定を行います。

1. AWS コンソールにログインしてください。
2. AWS コンソール上部の検索バーに「QuickSight」と入力し、表示された QuickSight のリンクをクリックします。
![](/static/04-dashboarding/option2-amazon-quicksight/aws-console-search-bar.png)
3. 「Sign up for QuickSight」ボタンをクリックします (初期設定済みの場合は次のセクションに進んでください)。
![](/static/04-dashboarding/option2-amazon-quicksight/sign-up-for-quicksight.png)
4. 「Enterprise」エディションを選択し、「Continue」ボタンをクリックします。
![](/static/04-dashboarding/option2-amazon-quicksight/create-your-quicksight-account.png)
5. Paginated Report add-on は今回必要ないので「No, Maybe Later」ボタンをクリックします。
![](/static/04-dashboarding/option2-amazon-quicksight/get-paginated-report-add-on.png)
6. 「Select a region」のボックスではワークショップを実施しているリージョンを選択し、「QuickSight account name」には任意の名前 (`databricks-on-aws-workshop-<your name>` など、一意である必要があります) を入力し、「Notification email address」にはあなたのメールアドレスを入力してください。その他はデフォルトの設定のままにし、「Finish」ボタンをクリックします。
![](/static/04-dashboarding/option2-amazon-quicksight/account-setting.png)
7. 初期設定が完了したら「Go to Amazon QuickSight」ボタンをクリックします。

## Amazon QuickSight の Databricks コネクターをセットアップ

1. Datasets
![](/static/04-dashboarding/option2-amazon-quicksight/quicksight-analyses.png)
2. New Dataset
![](/static/04-dashboarding/option2-amazon-quicksight/quicksight-datasets.png)
3. Databricks
![](/static/04-dashboarding/option2-amazon-quicksight/quicksight-connectors.png)

### Databricks クラスターへの JDBC 接続情報を確認

クラスターが起動状態であることを確認してください。

### QuickSight の Databricks コネクターを作成

![](/static/04-dashboarding/option2-amazon-quicksight/new-databricks-data-source.png)

## Amazon QuickSight でダッシュボードを作成

## 参考文献

- [Using Databricks in QuickSight](https://docs.aws.amazon.com/quicksight/latest/user/quicksight-databricks.html)
- [Amazon QuickSight Administrator's guide to connecting Databricks](https://docs.aws.amazon.com/quicksight/latest/user/quicksight-databricks-administration-setup.html)
- [Configure the Databricks ODBC and JDBC drivers](https://docs.databricks.com/integrations/jdbc-odbc-bi.html#get-server-hostname-port-http-path-and-jdbc-url)
