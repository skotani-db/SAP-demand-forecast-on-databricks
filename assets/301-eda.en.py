# Databricks notebook source
# MAGIC %md
# MAGIC # Exploratory Data Analysis (EDA) on Databricks
# MAGIC

# COMMAND ----------

catalog_name = "workshop_2998024384562747" # Rewrite
spark.conf.set("var.catalog_name", catalog_name)

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG ${var.catalog_name};
# MAGIC CREATE SCHEMA IF NOT EXISTS sap_seminar;
# MAGIC USE SCHEMA sap_seminar;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 1: Perform basic analysis
# MAGIC
# MAGIC First, let's check the basic statistics.
# MAGIC Run the following cell, click the plus sign on the right of the output Table tab, and click Data Profile.
# MAGIC You can automatically visualize statistics and histograms for each column.
# MAGIC
# MAGIC
# MAGIC For the following steps, enter and execute queries in the **SQL Editor** in the left pane.
# MAGIC When executing a query, you must specify the catalog and schema.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Basic statistics can be obtained by clicking the plus sign on the right of the Table tab → Data Profile
# MAGIC SELECT
# MAGIC *
# MAGIC FROM
# MAGIC sales_record_silver;

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2: Determine the items to be analyzed

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Aggregate the number of transactions and transaction amounts by product type
# MAGIC -- Click the triangle next to the column name in the table to sort
# MAGIC SELECT
# MAGIC ItemGroup,
# MAGIC SUM(Price),
# MAGIC COUNT(1)
# MAGIC FROM
# MAGIC sales_record_silver
# MAGIC GROUP BY
# MAGIC ItemGroup;

# COMMAND ----------

# MAGIC %md
# MAGIC Here, ZYOUTH, ZCRUISE, ZRACING, and ZMTN are the subjects of analysis because they have large transaction volumes and frequency. \
# MAGIC From the ItemGroup names, we can imagine that they refer to children's bicycles, mamachari, racing bicycles, and mountain bikes, respectively.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 3: Check the time series trends of the items to be analyzed

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC *,
# MAGIC date_format(RegisteredDate, 'yyyyMM') YearMonth
# MAGIC FROM
# MAGIC sales_record_silver
# MAGIC WHERE
# MAGIC ItemGroup in ("ZYOUTH", "ZCRUISE", "ZRACING", "ZMTN");

# COMMAND ----------

# MAGIC %md
# MAGIC For all the items to be analyzed, the transaction amount and frequency have been sluggish since April 2020. ZCRUISE is an exception, and we can see that sales spike about once every six months.

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 4: Create a feature table for AutoML
# MAGIC This time, the goal is to predict the monthly time series of overall bicycle sales.
# MAGIC Use Databricks' AutoML function to develop a sales prediction model.
# For MAGIC AutoML, create a `sales_history` table with columns for year, month, and sales amount.

# COMMAND ----------
# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE sales_history AS
# MAGIC SELECT
# MAGIC     YearMonth,
# MAGIC     SUM(Price) Price
# MAGIC FROM
# MAGIC  (
# MAGIC SELECT
# MAGIC  date_format (RegisteredDate, 'yyyy-MM-01') YearMonth,
# MAGIC  Price
# MAGIC FROM
# MAGIC  sales_record_silver
# MAGIC WHERE
# MAGIC  ItemGroup in ("ZYOUTH", "ZCRUISE", "ZRACING", "ZMTN")
# MAGIC ) item_extracted
# MAGIC GROUP BY
# MAGIC YearMonth

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM sales_history;

# COMMAND ----------

# MAGIC %md
# MAGIC Click the triangle mark next to the YearMonth column in the table that is displayed after executing the cell above to sort.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Oops!! Data from 2021-04-01 onwards has been mixed in, so let's delete it.
# MAGIC
# MAGIC Sales data from October 2017 to March 2021 is included, but for some reason, data from October 2022 has been mixed in.
# MAGIC Delete this data as it is not necessary for developing a sales forecast model.

# COMMAND ----------

# MAGIC %sql
# MAGIC DELETE FROM sales_history WHERE YearMonth > '2022-03-01'

# COMMAND ----------

# MAGIC %md
# MAGIC In Databricks Delta Lake, metadata is added to parquet files, and the history of operations on the table is saved.

# MAGIC Therefore, it is possible to restore (time travel) back to a version.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- The table version is created and time travel is possible

# MAGIC DESCRIBE HISTORY sales_history;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM sales_history;

# COMMAND ----------

# MAGIC %md
# MAGIC This completes the preparation of the table for machine learning model development. Please proceed to `302-machine-learning.ja`.


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
