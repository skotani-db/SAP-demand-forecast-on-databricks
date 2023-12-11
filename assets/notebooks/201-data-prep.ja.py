# Databricks notebook source
# MAGIC %md
# MAGIC ## Step 1: SAP データ抽出先の Amazon S3 バケットのマウント
# MAGIC Databricks において S3 バケットをデータソースとする方法はいくつかあります。
# MAGIC * Unity Catalog の外部ロケーション/Volumeを用いる (推奨)
# MAGIC * Instance Profile をクラスターにアタッチし、 S3 バケットを DBFS へマウントする
# MAGIC * Credential Paththrough によるアクセス
# MAGIC * Access Key 認証によるアクセス
# MAGIC
# MAGIC 今回は S3バケット　`<AWSAccountID>-appflowodata-<YYYYMMDD>` を Unity Catalogの外部ボリュームとして登録し、ファイルとして格納されている SAP データへアクセスします。
# MAGIC 一方で、事前準備で S3 フルアクセスの権限を持ったインスタンスプロファイルをクラスターにアタッチ済みです。このまま、DBFS (Databricks File System) にデータ抽出を行った S3 バケットをマウントしアクセスすることも可能です。事前準備セクションでセルフペースを選択し、Unity Catalogのセットアップを行っていない場合、こちらのオプションでデータニアクセスします。

# COMMAND ----------

# MAGIC %md
# MAGIC ### (推奨) Unity Catalog の外部ロケーション/Volumeを用いる 
# MAGIC Instance Profileはクラスターごとにアタッチする必要があり、 IAMロールでの権限管理になるため、Databricks の権限モデルから逸脱したアクセスコントロールになることが課題でした。複数のS3バケットへのアクセスを Instance Profileによって管理している場合、権限の変更が生じた際に直接 IAM Role を変更してなくてはならず運用が複雑化します。
# MAGIC
# MAGIC そこで、Unity Catalogで外部ロケーション/Volumeを用いることで、 事前に登録したS3バケットへのアクセスコントロールを Unity Catalog の権限モデル体系で管理できる様になります。あるS3バケットをユーザーにアクセスできなくしたい場合、 IAM Role を直接編集するのではなく、 Unity Catalog 側で権限を剥奪すれば良いのです。

# COMMAND ----------

# MAGIC %sql
# MAGIC -- カタログとスキーマの設定
# MAGIC USE CATALOG main;
# MAGIC CREATE SCHEMA IF NOT EXISTS sap_seminar;
# MAGIC USE SCHEMA sap_seminar;

# COMMAND ----------

# MAGIC %md
# MAGIC #### ストレージ認証情報を登録します
# MAGIC ストレージ認証情報は、AWS IAMロールを表すセキュリティ保護可能なオブジェクトです。
# MAGIC ストレージ資格情報が作成されると、その資格情報へのアクセス権を プリンシパル (ユーザーとグループ) に付与できます。
# MAGIC ストレージ資格情報は、主に、特定のストレージ パスへのアクセスをスコープする 外部ロケーションを作成するために使用されます。
# MAGIC 以下はストレージ認証情報を登録するためのステップです。
# MAGIC
# MAGIC 1. 左ペインから **Catalog** を選択します
# MAGIC 1. **Catalog Explorer** が表示されます。左下のメニュー **Storage Credential** を選択します
# MAGIC 1. **Create Credential** を選択します
# MAGIC 1. **Copy from Instance Profile** を選択し、 **databricks-cluster-sagemaker-acess-role** を選択します。
# MAGIC 1. **databricks-cluster-sagemaker-acess-role** のIAM Role ARNを入力し、**Create** を選択します

# COMMAND ----------

# MAGIC %md
# MAGIC #### 外部ロケーションを登録します
# MAGIC 外部ロケーションは、ストレージ・パスと、そのパスへのアクセスを承認するストレージ資格情報を組み合わせた、セキュリティ保護可能なオブジェクトです。
# MAGIC 外部ロケーションの作成者は、その最初の所有者です。 外部ロケーションの所有者は、外部ロケーションの名前、URI、およびストレージ資格情報を変更できます。
# MAGIC
# MAGIC 外部ロケーションを作成した後は、アカウントレベルの プリンシパル (ユーザーとグループ) にアクセス権を付与できます。
# MAGIC
# MAGIC 以下は外部ロケーションを登録するためのステップです。
# MAGIC
# MAGIC 1. 左ペインから **Catalog** を選択します
# MAGIC 1. **Catalog Explorer** が表示されます。左下のメニュー **External Locations** を選択します
# MAGIC 1. **Create Location** を選択します
# MAGIC 1. **Manual** を選択し、 **External Location name** には**sap-data**を指定し、**Storage credential**には前のステップで作成したものをプルダウンから選択し、**URL**にはデータ抽出先として指定した S3 バケットの名前 (`s3://111122223333-appflowodata-20230808` のような形式) を入力します。
# MAGIC 1. **Create** を選択します

# COMMAND ----------

# MAGIC %md
# MAGIC #### 外部ボリュームを作成します
# MAGIC ボリュームは、クラウドオブジェクトストレージロケーションのストレージの論理的ボリュームを表現するUnity Catalogのオブジェクトです。ボリュームは、ファイルのアクセス、格納、制御、整理する能力を提供します。テーブルは表形式のデータセットに対するガバナンスを提供しますが、ボリュームは非テーブルケー式のデータセットに対するガバナンスを追加します

# COMMAND ----------

# MAGIC %sql
# MAGIC -- ボリュームの作成
# MAGIC CREATE EXTERNAL VOLUME main.sap_seminar.sap_data
# MAGIC LOCATION "s3://675409449903-appflowodata-20230928";

# COMMAND ----------

# MAGIC %md
# MAGIC #### (TODO) Catalog Explorer でボリュームの所在を確認してみよう！

# COMMAND ----------

# MAGIC %md
# MAGIC ###  (参考) Instance Profile をクラスターにアタッチし、 S3 バケットを DBFS へマウントする

# COMMAND ----------

# MAGIC %md
# MAGIC 次のセルを選択した状態で Shift+Enter などを押すとセル内のコードを実行できます。

# COMMAND ----------

# ## Databricks Widgets で変数を取得

# # Amazon AppFlow でデータ抽出したバケット名
# dbutils.widgets.text("aws_bucket_name", "")

# COMMAND ----------

# MAGIC %md
# MAGIC 画面上部に `aws_bucket_name` というテキストボックスが表示されます。
# MAGIC テキストボックスに AppFlow のデータ抽出先として指定した S3 バケットの名前 (`111122223333-appflowodata-20230808` のような形式) を入力した上で、次のセルを実行してください。

# COMMAND ----------

# # mount時のフォルダ名を指定
# mount_name = dbutils.widgets.get("aws_bucket_name")

# # S3バケットのマウント
# dbutils.fs.mount(f"s3a://{mount_name}", f"/mnt/{mount_name}")
# display(dbutils.fs.ls(f"/mnt/{mount_name}"))

# COMMAND ----------

# MAGIC %md
# MAGIC マウントしたディレクトリのパス等を含んだテーブルが表示されれば成功です。
# MAGIC マウントを解除するには以下のセルをアンコメントして実行してください。

# COMMAND ----------

# # mount を解除する
# dbutils.fs.unmount(f"/mnt/{mount_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2:Spark Dataframe として抽出データをロードし、テーブル化

# COMMAND ----------

## データパス
# Volumeの場合
path = "/Volumes/main/sap_seminar/sap_data"
# Instance Profileの場合
# path = f"/mnt/{mount_name}"

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW VOLUMES

# COMMAND ----------

# VBAK : 伝票ヘッダー
df_vbak = (
    spark.read.option("inferSchema", True)
    .format("parquet")
    .load(f"{path}/salesheader/*")
)

# VBAP : 売上明細
df_vbap = (
    spark.read.option("inferSchema", True)
    .format("parquet")
    .load(f"{path}/salesitem/*")
)

# COMMAND ----------

# MAGIC %md
# MAGIC それぞれ `vbak_bronze`、`vbap_bronze` としてテーブル化します。

# COMMAND ----------

# VBAK
(df_vbak.write.format("delta").mode("overwrite").saveAsTable("vbak_bronze"))

# VBAP
(df_vbap.write.format("delta").mode("overwrite").saveAsTable("vbap_bronze"))

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   vbak_bronze;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   vbap_bronze;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 3: カラムマッピングファイルをテーブル化する
# MAGIC このままでは各列が何の情報を表しているか分からないため、参照用のマッピングファイルを準備しておきます。

# COMMAND ----------

# user nameの取得
user_name = spark.sql("SELECT current_user()").collect()[0][0]

# VBAK
(
    spark.read.format("csv")
    .option("header", True)
    .load(
        f"file:/Workspace/Users/{user_name}/vbak_mapping.csv"
    )
    .createOrReplaceTempView("vbak_mapping")
)

# VBAP
(
    spark.read.format("csv")
    .option("header", True)
    .load(
        f"file:/Workspace/Users/{user_name}/vbap_mapping.csv"
    )
    .createOrReplaceTempView("vbap_mapping")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### VBAK：伝票ヘッダーの主要なカラム
# MAGIC VBELN - 販売伝票 (番号) \
# MAGIC ERDAT - 登録日付 \
# MAGIC KUNNR - 受注先 \
# MAGIC NETWR - 受注正味額 \
# MAGIC WAERK - 販売伝票通貨

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   vbak_mapping;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   VBELN,
# MAGIC   ERDAT,
# MAGIC   KUNNR,
# MAGIC   NETWR,
# MAGIC   WAERK
# MAGIC FROM
# MAGIC   vbak_bronze;

# COMMAND ----------

# MAGIC %md
# MAGIC ### VBAP：商品明細の主要なカラム
# MAGIC VBELN - 販売伝票(番号) \
# MAGIC MATKL - 品目グループ \
# MAGIC VOLUM - 総数量 \
# MAGIC NETWR - 正味額　\
# MAGIC WAERK - 販売伝票通貨

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   vbap_mapping;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   VBELN,
# MAGIC   MATKL,
# MAGIC   VOLUM,
# MAGIC   NETWR,
# MAGIC   WAERK
# MAGIC FROM
# MAGIC   vbap_bronze;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 4: 売上予測の分析に必要な情報を持ったエンリッチデータを作成する
# MAGIC

# COMMAND ----------

from pyspark.sql.functions import *

# 伝票ヘッダーからは伝票番号、登録日、通貨、顧客をセレクト
df_vbak_renamed = (
    spark.read.table("vbak_bronze")
    .withColumnRenamed("VBELN", "ID")
    .withColumn("RegisteredDate", to_date(col("ERDAT")))
    .withColumnRenamed("KUNNR", "Customer")
    .withColumnRenamed("WAERK", "Currency")
    .select("ID", "RegisteredDate", "Currency", "Customer")
)

display(df_vbak_renamed)

# COMMAND ----------

# 商品明細からは伝票番号、正味額、品目をセレクト
df_vbap_renamed = (
    spark.read.table("vbap_bronze")
    .withColumnRenamed("VBELN", "ID")
    .withColumnRenamed("NETWR", "Price")
    .withColumnRenamed("MATKL", "ItemGroup")
    .select("ID", "Price", "ItemGroup")
)

display(df_vbap_renamed)

# COMMAND ----------

# 品目情報が取れるレコードのみを残して、売上に関するエンリッチデータを作成する
(
    df_vbak_renamed.join(df_vbap_renamed, on="ID", how="inner")
    .write.format("delta")
    .mode("overwrite")
    .saveAsTable("sales_record_silver")
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   sales_record_silver

# COMMAND ----------

# MAGIC %md
# MAGIC これで初期のデータ準備は完了です。
# MAGIC 「Lab 3: Databricks と MLflow を用いた需要予測モデル開発」に進んでください。

# COMMAND ----------

# MAGIC %md
# MAGIC ## LICENSE
# MAGIC
# MAGIC MIT No Attribution
# MAGIC
# MAGIC Copyright 2023 Amazon Web Services Japan G.K.
# MAGIC
# MAGIC Permission is hereby granted, free of charge, to any person obtaining a copy of this
# MAGIC software and associated documentation files (the "Software"), to deal in the Software
# MAGIC without restriction, including without limitation the rights to use, copy, modify,
# MAGIC merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# MAGIC permit persons to whom the Software is furnished to do so.
# MAGIC
# MAGIC THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# MAGIC INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# MAGIC PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# MAGIC HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# MAGIC OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# MAGIC SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
