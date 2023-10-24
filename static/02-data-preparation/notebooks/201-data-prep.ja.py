# Databricks notebook source
# MAGIC %md
# MAGIC ## Step 1: SAP データ抽出先の Amazon S3 バケットのマウント
# MAGIC Databricks において S3 バケットをデータソースとする方法はいくつかあります。
# MAGIC * Unity Catalog の外部ロケーションを用いる (推奨)
# MAGIC * Instance Profile をクラスターにアタッチする
# MAGIC * Credential Paththrough によるアクセス
# MAGIC * Access Key 認証によるアクセス
# MAGIC
# MAGIC 今回は事前準備で S3 フルアクセスの権限を持ったインスタンスプロファイルをクラスターにアタッチ済みなので、このまま、DBFS (Databricks File System) にデータ抽出を行った S3 バケットをマウントします。

# COMMAND ----------

# MAGIC %md
# MAGIC 次のセルを選択した状態で Shift+Enter などを押すとセル内のコードを実行できます。

# COMMAND ----------

## Databricks Widgets で変数を取得

# Amazon AppFlow でデータ抽出したバケット名
dbutils.widgets.text("aws_bucket_name", "")

# COMMAND ----------

# MAGIC %md
# MAGIC 画面上部に `aws_bucket_name` というテキストボックスが表示されます。
# MAGIC テキストボックスに AppFlow のデータ抽出先として指定した S3 バケットの名前 (`111122223333-appflowodata-20230808` のような形式) を入力した上で、次のセルを実行してください。

# COMMAND ----------

# mount時のフォルダ名を指定
mount_name = dbutils.widgets.get("aws_bucket_name")

# S3バケットのマウント
dbutils.fs.mount(f"s3a://{mount_name}", f"/mnt/{mount_name}")
display(dbutils.fs.ls(f"/mnt/{mount_name}"))

# COMMAND ----------

# MAGIC %md
# MAGIC マウントしたディレクトリのパス等を含んだテーブルが表示されれば成功です。
# MAGIC マウントを解除するには以下のセルをアンコメントして実行してください。

# COMMAND ----------

# mount を解除する
# dbutils.fs.unmount(f"/mnt/{mount_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2:Spark Dataframe として抽出データをロードし、テーブル化

# COMMAND ----------

# VBAK : 伝票ヘッダー
df_vbak = (
    spark.read.option("inferSchema", True)
    .format("parquet")
    .load("/mnt/%s/salesheader/*" % mount_name)
)

# VBAP : 売上明細
df_vbap = (
    spark.read.option("inferSchema", True)
    .format("parquet")
    .load("/mnt/%s/salesitem/*" % mount_name)
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
