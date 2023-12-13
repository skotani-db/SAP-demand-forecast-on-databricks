-- Databricks notebook source
-- catalog_nameが変数で入力される前提
CREATE OR REFRESH STREAMING LIVE TABLE dlt_vbak_raw AS
SELECT
  current_timestamp() processing_time,
  *
FROM
  cloud_files(
    "dbfs:/Volumes/${catalog_name}/${schema_name}/sap_data/salesheader/*",
    "parquet"
  );

-- COMMAND ----------

-- catalog_nameが変数で入力される前提
CREATE OR REFRESH STREAMING LIVE TABLE dlt_vbap_raw AS
SELECT
  current_timestamp() processing_time,
  *
FROM
  cloud_files(
    "dbfs:/Volumes/${catalog_name}/${schema_name}/sap_data/salesitem/*",
    "parquet"
  );

-- COMMAND ----------

-- 伝票ヘッダーからは伝票番号、登録日、通貨、顧客をセレクト
CREATE OR REFRESH STREAMING LIVE TABLE dlt_vbak_bronze AS
SELECT VBELN as ID, TO_DATE(ERDAT) as RegisteredDate, WAERK as Currency, KUNNR as Customer 
FROM STREAM(LIVE.dlt_vbak_raw)

-- COMMAND ----------

-- 商品明細からは伝票番号、正味額、品目をセレクト
CREATE OR REFRESH STREAMING LIVE TABLE dlt_vbap_bronze AS
SELECT VBELN AS ID, NETWR AS Price, MATKL AS ItemGroup
FROM STREAM(LIVE.dlt_vbap_raw)

-- COMMAND ----------

CREATE OR REFRESH LIVE TABLE dlt_sales_record_silver AS
SELECT k.ID ID, Price, ItemGroup, RegisteredDate, Currency, Customer
FROM LIVE.dlt_vbak_bronze k
INNER JOIN LIVE.dlt_vbap_bronze p
ON k.ID = p.ID
