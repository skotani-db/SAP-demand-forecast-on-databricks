# Databricks notebook source
# MAGIC %sql
# MAGIC -- 実績と予測を盛り込んだテーブルを作成する
# MAGIC CREATE OR REPLACE TABLE sales_forecast
# MAGIC     (YearMonth, Price, Price_lower, Price_upper)
# MAGIC AS SELECT YearMonth, Price, NULL Price_lower, NULL Price_upper
# MAGIC       FROM sales_history
# MAGIC UNION ALL
# MAGIC SELECT LEFT(YearMonth, 10), Price, Price_lower, Price_upper
# MAGIC       FROM forecast_prediction_xxxxxx;
# MAGIC
# MAGIC SELECT * FROM sales_forecast;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- 品種別の取引回数と取引額を集計
# MAGIC SELECT
# MAGIC   ItemGroup,
# MAGIC   SUM(Price),
# MAGIC   COUNT(1)
# MAGIC FROM
# MAGIC   sales_record_silver
# MAGIC GROUP BY
# MAGIC   ItemGroup;

# COMMAND ----------

# MAGIC %sql
# MAGIC -- 
# MAGIC SELECT
# MAGIC   *,
# MAGIC   date_format(RegisteredDate, 'yyyyMM') YearMonth
# MAGIC FROM
# MAGIC   sales_record_silver
# MAGIC WHERE
# MAGIC   ItemGroup in ("ZYOUTH", "ZCRUISE", "ZRACING", "ZMTN");
