# Databricks notebook source
# MAGIC %md-sandbox ### DatabricksのAuto MLと`sales_history`テーブルの使用
# MAGIC
# MAGIC <img style="float: right" width="600" src='file:/Workspace/Repos/firstgrade430@gmail.com/SAP-demand-forecast-on-databricks/static/03-machine-learning/automl-setting.png'>
# MAGIC
# MAGIC Auto MLは、「Machine Learning(機械学習)」メニュースペースで利用できます。<br>
# MAGIC (Machine Learning メニューを選択し、ホーム画面で AutoMLを選択してください)
# MAGIC
# MAGIC 新規にAuto-ML実験を開始し、先ほど作成した特徴量テーブル(`sales_history`)を選択するだけで良いのです。
# MAGIC
# MAGIC ML Problem typeは、今回は`Forcasting`です。
# MAGIC prediction targetは`Price`カラムです。
# MAGIC Time columnは`YearMonth`カラムです。
# MAGIC Output Databaseは`default`です。
# MAGIC
# MAGIC AutoMLのMetricや実行時間とトライアル回数については、Advance Menuで選択できます。
# MAGIC
# MAGIC Forecast horizon and frequency(予測対象の期間)は`2` ヶ月とします
# MAGIC
# MAGIC Startをクリックすると、あとはDatabricksがやってくれます。
# MAGIC
# MAGIC この作業はUIで行いますが[python API](https://docs.databricks.com/applications/machine-learning/automl.html#automl-python-api-1)による操作も可能です。

# COMMAND ----------


