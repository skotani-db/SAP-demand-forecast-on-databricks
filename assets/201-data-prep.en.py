# Databricks notebook source
# MAGIC %md
# MAGIC ## Step 1: Mount the Amazon S3 bucket for SAP data extraction
# MAGIC There are several ways to make an S3 bucket a data source in Databricks.
# MAGIC * Using an external location/volume in the Unity Catalog (recommended)
# MAGIC * Attach the Instance Profile to the cluster and mount the S3 bucket to DBFS
# MAGIC * Access via Credential Paththrough
# MAGIC * Access via Access Key authentication
# MAGIC
# MAGIC This time, we will register the S3 bucket `<AWSAccountID>-appflowodata-<YYYYMMDD>` as an external volume in the Unity Catalog and access the SAP data stored as files.
# MAGIC On the other hand, you have already attached an instance profile with full S3 access permissions to the cluster during the preparation. You can also mount the S3 bucket where you extracted the data to DBFS (Databricks File System) and access it. If you selected Self-paced in the Preparation section and have not set up Unity Catalog, you can access the data with this option.
# COMMAND ----------

# MAGIC %md
# MAGIC ### (Recommended) Use an external location/volume in the Unity Catalog
# MAGIC An Instance Profile needs to be attached to each cluster, and because permissions are managed by IAM roles, the access control deviates from the Databricks permission model, which was an issue. If you manage access to multiple S3 buckets with an Instance Profile, you have to change the IAM Role directly when permissions change, which makes operations complicated.
# MAGIC
# MAGIC Therefore, by using an external location/volume in Unity Catalog, you can manage access control to pre-registered S3 buckets using the Unity Catalog permission model. If you want to prevent a user from accessing a certain S3 bucket, you can revoke the permission on the Unity Catalog side instead of directly editing the IAM Role.
# MAGIC
# MAGIC Select **Catalog** from the left pane and copy the catalog name that contains the workspace name (e.g. `workshop_2998024384562747`) and replace the following cell with it.

# COMMAND ----------

catalog_name = "workshop_2998024384562747" # Rewrite
spark.conf.set("var.catalog_name", catalog_name)

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Catalog and schema settings
# MAGIC USE CATALOG ${var.catalog_name};
# MAGIC CREATE SCHEMA IF NOT EXISTS sap_seminar;
# MAGIC USE SCHEMA sap_seminar;

# COMMAND ----------

# MAGIC %md
# MAGIC #### Register storage credentials
# MAGIC A storage credential is a securable object that represents an AWS IAM role.
# MAGIC Once a storage credential is created, you can grant principals (users and groups) access to it.
# MAGIC Storage credentials are primarily used to create an external location that scopes access to a specific storage path.
# MAGIC Below are the steps to register storage credentials.
# MAGIC
# MAGIC 1. Select **Catalog** from the left pane
# MAGIC 1. The **Catalog Explorer** will be displayed. Open the bottom left menu **External Data** and select **Storage Credential**
# MAGIC 1. Select **Create Credential**
# MAGIC 1. Select **Copy from Instance Profile**, and then select **databricks-cluster-sagemaker-acess-role**.
# MAGIC 1. Enter the IAM Role ARN for **databricks-cluster-sagemaker-acess-role** (`arn:aws:iam::<AWS Account ID>:role/databricks-cluster-sagemaker-access-role`) and choose **Create**.

# COMMAND ----------

# MAGIC %md
# MAGIC #### Register an external location
# MAGIC An external location is a securable object that combines a storage path with storage credentials that authorize access to that path.
# MAGIC The creator of an external location is its initial owner. The owner of an external location can modify the name, URI, and storage credentials of the external location.
# MAGIC
# MAGIC After you create an external location, you can grant access to account-level principals (users and groups).
# MAGIC
# MAGIC Below are the steps to register an external location.
# MAGIC
# MAGIC 1. Select **Catalog** from the left pane
# MAGIC 1. The **Catalog Explorer** will be displayed. Open the bottom left menu **External Data** and select **External Locations**
# MAGIC 1. Select **Create Location**
# MAGIC 1. Select **Manual**, specify **sap-data** for **External Location name**, select `databricks-cluster-sagemaker-access-role` created in the previous step from the drop-down list for **Storage credentials**, and enter the name of the S3 bucket you specified as the data destination for **URL** (in the format of `s3://111122223333-appflowodata-20230808`).
# MAGIC 1. Select **Create**

# COMMAND ----------

# MAGIC %md
# MAGIC #### Create an external volume
# MAGIC A Volume is an object in the Unity Catalog that represents a logical volume of storage in a cloud object storage location. Volumes provide the ability to access, store, control, and organize files. While tables provide governance over tabular data sets, volumes add governance over non-table-based data sets.

# COMMAND ----------

# MAGIC %sql
# MAGIC -- Creating a Volume
# MAGIC CREATE EXTERNAL VOLUME ${var.catalog_name}.sap_seminar.sap_data
# MAGIC LOCATION "s3://501563350435-appflowodata-20231213";  -- rewrite

# COMMAND ----------

# MAGIC %md
# MAGIC #### (TODO) Let's check the location of the volume in Catalog Explorer!

# COMMAND ----------

# MAGIC %md
# MAGIC ###  (Reference) Attach an Instance Profile to a cluster and mount an S3 bucket to DBFS

# COMMAND ----------

# MAGIC %md
# MAGIC With the next cell selected, you can press Shift+Enter or similar to execute the code in the cell.

# COMMAND ----------

# ## Get variables in Databricks Widgets

# # Bucket name where data was extracted using Amazon AppFlow
# dbutils.widgets.text("aws_bucket_name", "")

# COMMAND ----------

# MAGIC %md
# MAGIC A text box labeled `aws_bucket_name` will appear at the top of the screen.
# MAGIC Enter the name of the S3 bucket you specified as the AppFlow data destination in the text box (in a format similar to `111122223333-appflowodata-20230808`), and then run the following cell.

# COMMAND ----------

# # Specify the folder name when mounting
# mount_name = dbutils.widgets.get("aws_bucket_name")

# # Mounting an S3 bucket
# dbutils.fs.mount(f"s3a://{mount_name}", f"/mnt/{mount_name}")
# display(dbutils.fs.ls(f"/mnt/{mount_name}"))

# COMMAND ----------

# MAGIC %md
# MAGIC If a table containing the path of the mounted directory is displayed, the operation was successful.
# MAGIC To unmount, uncomment and run the following cell:

# COMMAND ----------

# # Unmount
# dbutils.fs.unmount(f"/mnt/{mount_name}")

# COMMAND ----------

# MAGIC %md
# MAGIC ## Step 2: Load the extracted data as a Spark Dataframe

# COMMAND ----------

## Data Path
# For Volume
path = f"/Volumes/{catalog_name}/sap_seminar/sap_data"
# For Instance Profile
# path = f"/mnt/{mount_name}"

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW VOLUMES

# COMMAND ----------

# VBAK : Document Header
df_vbak = (
    spark.read.option("inferSchema", True)
    .format("parquet")
    .load(f"{path}/salesheader/*")
)

# VBAP : Sales details
df_vbap = (
    spark.read.option("inferSchema", True)
    .format("parquet")
    .load(f"{path}/salesitem/*")
)

# COMMAND ----------

# MAGIC %md
# MAGIC They will be tabulated as `vbak_bronze` and `vbap_bronze` respectively.

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
# MAGIC ## Step 3: Table column mapping file
# MAGIC As it is, it is not clear what information each column represents, so we will prepare a mapping file for reference.

# COMMAND ----------

# Get user name
user_name = spark.sql("SELECT current_user()").collect()[0][0]

# VBAK
(
    spark.read.format("csv")
    .option("header", True)
    .load(
        f"file:/Workspace/Repos/{user_name}/SAP-demand-forecast-on-databricks/assets/vbak_mapping.csv"
    )
    .createOrReplaceTempView("vbak_mapping")
)

# VBAP
(
    spark.read.format("csv")
    .option("header", True)
    .load(
        f"file:/Workspace/Repos/{user_name}/SAP-demand-forecast-on-databricks/assets/vbap_mapping.csv"
    )
    .createOrReplaceTempView("vbap_mapping")
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### VBAK: Document Header Key Columns
# MAGIC VBELN - Sales document (number) \
# MAGIC ERDAT - Registration Date \
# MAGIC KUNNR - Customer \
# MAGIC NETWR - Net order amount \
# MAGIC WAERK - Sales document currency

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
# MAGIC ### VBAP: Key columns of product details
# MAGIC VBELN - Sales slip (number) \
# MAGIC MATKL - Item Group \
# MAGIC VOLUM - Total Quantity \
# MAGIC NETWR - Net amount \
# MAGIC WAERK - Sales document currency

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
# MAGIC ## Step 4: Create enriched data with the information you need to analyse sales forecasts
# MAGIC

# COMMAND ----------

from pyspark.sql.functions import *

# Select the document number, entry date, currency, and customer from the document header.
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

# Select the invoice number, net amount, and item from the product details
df_vbap_renamed = (
    spark.read.table("vbap_bronze")
    .withColumnRenamed("VBELN", "ID")
    .withColumnRenamed("NETWR", "Price")
    .withColumnRenamed("MATKL", "ItemGroup")
    .select("ID", "Price", "ItemGroup")
)

display(df_vbap_renamed)

# COMMAND ----------

# Create enriched sales data by keeping only records that contain item information
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
# MAGIC This completes the initial data preparation.
# MAGIC Continue to Lab 3: Developing a Demand Forecasting Model with Databricks and MLflow.

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
