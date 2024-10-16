# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC ## Using Databricks Auto ML with the `sales_history` table
# MAGIC
# MAGIC <img style="float: right" width="600" src='https://github.com/skotani-db/SAP-demand-forecast-on-databricks/blob/main/static/03-machine-learning/automl-setting.png?raw=true'>
# MAGIC
# MAGIC Auto ML is available in the Machine Learning menu space. <br>
# MAGIC (Select Experiments under the Machine Learning section in the left pane.)
# MAGIC
# MAGIC Click the "Create AutoML Experiment" button to start a new Auto-ML experiment, and simply select the feature table you just created (e.g. `workshop_2998024384562747.sap_seminar.sales_history`) to automatically train the model.
# MAGIC
# The MAGIC ML Problem type is `Forcasting` this time. \
# The MAGIC prediction target is the `Price` column. \
# The MAGIC Time column is the `YearMonth` column. \
# The MAGIC Output Database is `workshop_2998024384562747.sap_seminar`.
# MAGIC
# MAGIC Forecast horizon and frequency (forecast period) is set to `2` months
# MAGIC
# MAGIC AutoML metrics, execution time, and number of trials can be selected in the "Advance Menu (optional)".
# MAGIC
# MAGIC This time, set "Timeout (minutes)" to `5` minutes to shorten the time.
# MAGIC
# MAGIC Click Start, and Databricks will do the rest.
# MAGIC
# MAGIC This task is done in the UI, but it can also be performed using the [python API](https://docs.databricks.com/applications/machine-learning/automl.html#automl-python-api-1).

# COMMAND ----------

# MAGIC %md ## The progress and results of the experiment can be viewed on the MLflow Experiment screen.
# MAGIC
# MAGIC If you cannot see the experiment results after a while, click the refresh icon on the right side of the screen.
# MAGIC
# MAGIC <img src='https://github.com/skotani-db/SAP-demand-forecast-on-databricks/blob/main/static/03-machine-learning/experiment.png?raw=true' />

# COMMAND ----------

# MAGIC %md ## Notes
# MAGIC
# MAGIC - AutoML experiments are performed on a single node, so if the memory size is small, the number of datasets that can be learned will be small. Therefore, select an instance with a large memory capacity.
# MAGIC - Check the Warning tab in the above figure (MLflow Experiment UI).
# MAGIC - The following is an example

# MAGIC

# MAGIC <img src='https://raw.githubusercontent.com/microsoft/openhack-for-lakehouse-japanese/main/images/day2_02__automl/tutoml_alert.png' />

# COMMAND ----------

# MAGIC %md ## After AutoML is completed

# COMMAND ----------

# MAGIC %md
# MAGIC Check the displayed results and press compare

# MAGIC <img src='https://github.com/skotani-db/SAP-demand-forecast-on-databricks/blob/main/static/03-machine-learning/compare.png?raw=true' />

# COMMAND ----------

# MAGIC %md ## Compare the metrics for each model

# COMMAND ----------

# MAGIC %md
# MAGIC
# MAGIC <img src='https://github.com/skotani-db/SAP-demand-forecast-on-databricks/blob/main/static/03-machine-learning/metrics.png?raw=true' />

# COMMAND ----------

# MAGIC %md ## Register the created model in MLflow Model Registry
# MAGIC
# MAGIC Open the Run with the best score and register the trained model in Model Registry.
# MAGIC <br>
# MAGIC </br>
# MAGIC <img src='https://raw.githubusercontent.com/microsoft/openhack-for-lakehouse-japanese/main/images/day2_01__mlflow/mlflow-first.png' />
# MAGIC <br>
# MAGIC </br>
# MAGIC
# MAGIC **Please enter your name in the model name**
# MAGIC
# MAGIC <img src='https://raw.githubusercontent.com/microsoft/openhack-for-lakehouse-japanese/main/images/day2_01__mlflow/register_model.jpg' />
# MAGIC <br>
# MAGIC </br>
# MAGIC
# MAGIC **Click on the red frame**
# MAGIC <img src='https://raw.githubusercontent.com/microsoft/openhack-for-lakehouse-japanese/main/images/day2_01__mlflow/regist_model2.jpg' />
# MAGIC <br>
# MAGIC </br>
# MAGIC
# MAGIC **Click Transit to production**
# MAGIC <img src='https://raw.githubusercontent.com/microsoft/openhack-for-lakehouse-japanese/main/images/day2_01__mlflow/mlflow-second.png' />
# MAGIC <br>
# MAGIC </br>
# MAGIC **By performing this task, the model will be registered in the Databricks Model Registry, and it will be possible to call it from the mlflow API or spark. You can also check the details of the model from "Models" on the sidebar**

# COMMAND ----------

# MAGIC %md ## Create a data mart to check predictions and results
# MAGIC
# MAGIC Create a table that combines results and predictions to be used in "Lab 4: Visualization Dashboard Development".

# COMMAND ----------

catalog_name = "workshop_2998024384562747" # Rewrite
spark.conf.set("var.catalog_name", catalog_name)

# COMMAND ----------

# MAGIC %sql
# MAGIC USE CATALOG ${var.catalog_name};
# MAGIC CREATE SCHEMA IF NOT EXISTS sap_seminar;
# MAGIC USE SCHEMA sap_seminar;

# COMMAND ----------

# Identify forecast table
forecast_table_name = (
spark
.sql("SHOW TABLES")
.filter("tableName like 'forecast_prediction_%'")
.select("tableName")
.collect()
)[0][0]

display(forecast_table_name)

# COMMAND ----------

# Combine actuals and forecasts
prediction_table_query = f"""
CREATE OR REPLACE TABLE sales_forecast
AS SELECT YearMonth, Price, NULL Price_lower, NULL Price_upper
FROM sales_history
UNION ALL
SELECT LEFT(YearMonth, 10), Price, Price_lower, Price_upper
FROM {forecast_table_name};
"""

spark.sql(prediction_table_query)

# COMMAND ----------

# MAGIC %md
# MAGIC This completes the development of the machine learning model and the creation of the data mart.
# MAGIC
# MAGIC Return to the workshop page and proceed to the section "Deploying from MLflow Model Registry to Amazon SageMaker" or proceed to "Lab 4: Visualization Dashboard Development".

# COMMAND ----------

# MAGIC %md
# MAGIC ## LICENSE
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
