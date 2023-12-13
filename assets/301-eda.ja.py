# Databricks notebook source
# MAGIC %md
# MAGIC # Databricks 上での探索的データ分析 (Exploratory Data Analysis; EDA)
# MAGIC ## Step 1: 基礎分析を行う
# MAGIC
# MAGIC まずは基礎的な統計情報を確認してみましょう。
# MAGIC 次のセルを実行し、出力の Table タブ右のプラスマークをクリックし、Data Profile をクリックしてください。
# MAGIC 自動的に各カラムの統計情報とヒストグラム等の可視化を行うことができます。

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Table タブ右のプラスマーク → Data Profile で基礎統計が取得可能
# MAGIC SELECT
# MAGIC   *
# MAGIC FROM
# MAGIC   dlt_sales_record_silver;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2: 分析対象とする品目を決定する

# COMMAND ----------

# MAGIC %sql
# MAGIC -- 品種別の取引回数と取引額を集計
# MAGIC -- テーブルのカラム名横の三角をクリックするとソート可能
# MAGIC SELECT
# MAGIC   ItemGroup,
# MAGIC   SUM(Price),
# MAGIC   COUNT(1)
# MAGIC FROM
# MAGIC   dlt_sales_record_silver
# MAGIC GROUP BY
# MAGIC   ItemGroup;

# COMMAND ----------

# MAGIC %md
# MAGIC ここでは、ZYOUTH, ZCRUISE, ZRACING, ZMTN がそれぞれ取引規模・回数も大きいため、分析対象とします。 \
# MAGIC ItemGroup 名からそれぞれ子供向け自転車、ママチャリ、競技用、マウンテンバイクを指すものであると想像できます。

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 3: 分析対象となる品目の時系列推移を確認する

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC   *,
# MAGIC   date_format(RegisteredDate, 'yyyyMM') YearMonth
# MAGIC FROM
# MAGIC   dlt_sales_record_silver
# MAGIC WHERE
# MAGIC   ItemGroup in ("ZYOUTH", "ZCRUISE", "ZRACING", "ZMTN");

# COMMAND ----------

# MAGIC %md
# MAGIC 分析対象のすべての品種で2020年4月を境に取引額・回数ともに低調。ZCRUISE が例外で半年に一度ぐらいの頻度で売上がスパイクすることがあることがわかります。

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 4: AutoML 用の特徴量テーブルを作成する
# MAGIC 今回は自転車全体の売上を月毎の時系列で予測するのをゴールとします。
# MAGIC 売上予測のモデル開発は Databricks の AutoML 機能を用います。
# MAGIC AutoML 用に、年月と売上金額をカラムにもった `sales_history` テーブルを作成します。

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
# MAGIC       dlt_sales_record_silver
# MAGIC     WHERE
# MAGIC       ItemGroup in ("ZYOUTH", "ZCRUISE", "ZRACING", "ZMTN")
# MAGIC   ) item_extracted
# MAGIC GROUP BY
# MAGIC   YearMonth

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM sales_history;

# COMMAND ----------

# MAGIC %md
# MAGIC 上のセルを実行した結果表示されるテーブルの YearMonth カラムの横にある三角マークをクリックするとソートできます。

# COMMAND ----------

# MAGIC %md
# MAGIC ### Oops!! 2021-04-01 以降のデータが紛れ込んでしまっているので削除しよう
# MAGIC
# MAGIC 2017年10月から2021年3月までの売上データが含まれていますが、なぜか少し飛んで2022年10月のデータが紛れています。
# MAGIC 売上予測モデル開発に不要なデータのため削除します。

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM sales_history WHERE YearMonth > '2022-03-01'

# COMMAND ----------

# MAGIC %md
# MAGIC Databricks の Delta Lake では parquet ファイルにメタデータが付与されており、テーブルに対する操作の履歴が保存されます。
# MAGIC そのため、バージョンを遡って復元 (タイムトラベル) することも可能です。 

# COMMAND ----------

# MAGIC %sql
# MAGIC -- tableのversionがされ、タイムトラベル可能
# MAGIC DESCRIBE HISTORY sales_history;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM sales_history;

# COMMAND ----------

# MAGIC %md
# MAGIC これで機械学習モデル開発用のテーブルの準備は完了です。`302-machine-learning.ja.py` に進んでください。

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
