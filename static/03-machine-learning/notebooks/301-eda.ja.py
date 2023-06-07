# Databricks notebook source
# MAGIC %md
# MAGIC ### Step 1:基礎分析を行う

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Tableタブ右のプラスマーク→Data Profileで基礎統計が取得可能
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   sales_record_silver;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2:分析対象とする品目を決定する

# COMMAND ----------

# MAGIC %sql
# MAGIC -- 品種別の取引回数と取引額を集計
# MAGIC -- テーブルのカラム名横の三角をクリックするとソート可能
# MAGIC SELECT
# MAGIC   ItemGroup,
# MAGIC   SUM(Price),
# MAGIC   COUNT(1)
# MAGIC FROM
# MAGIC   sales_record_silver
# MAGIC GROUP BY
# MAGIC   ItemGroup;

# COMMAND ----------

# MAGIC %md
# MAGIC ZYOUTH, ZCRUISE, ZRACING, ZMTNがそれぞれ取引規模・回数も大きいため、分析対象とする。 \
# MAGIC それぞれ子供向け、ママチャリ、競技用、マウンテンバイクをItemGroup名から連想する。

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 3:分析対象となる品目の時系列推移を確認する

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   *,
# MAGIC   date_format(RegisteredDate, 'yyyyMM') YearMonth
# MAGIC FROM
# MAGIC   sales_record_silver
# MAGIC WHERE
# MAGIC   ItemGroup in ("ZYOUTH", "ZCRUISE", "ZRACING", "ZMTN");

# COMMAND ----------

# MAGIC %md
# MAGIC 分析対象のすべての品種で　２０２０年4月を境に取引額・回数ともに低調。ZCRUISEが例外で半年に一度ぐらいの頻度で売上がスパイクすることがある。

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 4:AutoML用の特徴量テーブルを作成する

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE sales_history AS
# MAGIC SELECT
# MAGIC   YearMonth,
# MAGIC   SUM(Price) Price
# MAGIC FROM
# MAGIC   (
# MAGIC     SELECT
# MAGIC       date_format(RegisteredDate, 'yyyy-MM-01') YearMonth,
# MAGIC       Price
# MAGIC     FROM
# MAGIC       sales_record_silver
# MAGIC     WHERE
# MAGIC       ItemGroup in ("ZYOUTH", "ZCRUISE", "ZRACING", "ZMTN")
# MAGIC   ) item_extracted
# MAGIC GROUP BY
# MAGIC   YearMonth

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM sales_history;
