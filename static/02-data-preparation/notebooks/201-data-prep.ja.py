# Databricks notebook source
# MAGIC %md
# MAGIC ## Step 1:データを抽出したS3バケットのマウント
# MAGIC Databricks において S3 バケットをデータソースとする方法はいくつかあります。
# MAGIC * Unity Catalog の外部ロケーションを用いる (推奨)
# MAGIC * Instance Profile をクラスターにアタッチする
# MAGIC * Credential Paththrough によるアクセス
# MAGIC * Access Key 認証によるアクセス
# MAGIC
# MAGIC 今回は事前準備で S3 フルアクセスの権限を持ったインスタンスプロファイルをクラスターにアタッチ済みなので、このまま、DBFS (Databricks File System) にデータ抽出を行った S3 バケットをマウントします。

# COMMAND ----------

## Databricks Widgets で変数を取得

# Appflow でデータ抽出したバケット名
dbutils.widgets.text("aws_bucket_name", "")

# COMMAND ----------

# mount時のフォルダ名を指定
mount_name = dbutils.widgets.get("aws_bucket_name")

# S3バケットのマウント
dbutils.fs.mount(
    f"s3a://{mount_name}", f"/mnt/{mount_name}"
)
display(dbutils.fs.ls(f"/mnt/{mount_name}"))

# COMMAND ----------

# mountを解除する
# dbutils.fs.unmount(f"/mnt/{mount_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2:Spark Dataframeとして抽出データをロードし、テーブル化

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
# MAGIC ## Step 3: GUIからカラムマッピングファイルをインポートして、テーブル化する
# MAGIC このままでは各列が何の情報を表しているか分からないため、マッピングファイルを活用する

# COMMAND ----------

# VBAK
(
    spark
    .read
    .format("csv")
    .load("file:/Workspace/Repos/<!!!your-email-address!!!>/SAP-demand-forecast-on-databricks/static/02-data-preparation/notebooks/vbak_mapping.csv")
    .createOrReplaceTempView("vbak_mapping")
)

# VBAP
(
    spark
    .read
    .format("csv")
    .load("file:/Workspace/Repos/<!!!your-email-address!!!>/SAP-demand-forecast-on-databricks/static/02-data-preparation/notebooks/vbak_mapping.csv")
    .createOrReplaceTempView("vbap_mapping")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### VBAK：伝票ヘッダーの主要なカラム
# MAGIC VBELN - 販売伝票(番号) \
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

# 伝票ヘッダーからは伝票番号、登録日、通貨、顧客
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

# 商品明細からは伝票番号、正味額、品目
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


