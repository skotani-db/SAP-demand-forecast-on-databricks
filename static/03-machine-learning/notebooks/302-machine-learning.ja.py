# Databricks notebook source
# MAGIC %md-sandbox ### DatabricksのAuto MLと`sales_history`テーブルの使用
# MAGIC
# MAGIC <img style="float: right" width="600" src='https://github.com/skotani-db/SAP-demand-forecast-on-databricks/blob/main/static/03-machine-learning/automl-setting.png?raw=true'>
# MAGIC
# MAGIC Auto MLは、「Machine Learning(機械学習)」メニュースペースで利用できます。<br>
# MAGIC (Machine Learning メニューを選択し、ホーム画面で AutoMLを選択してください)
# MAGIC
# MAGIC 新規にAuto-ML実験を開始し、先ほど作成した特徴量テーブル(`sales_history`)を選択するだけで良いのです。
# MAGIC
# MAGIC ML Problem typeは、今回は`Forcasting`です。 \
# MAGIC prediction targetは`Price`カラムです。 \
# MAGIC Time columnは`YearMonth`カラムです。 \
# MAGIC Output Databaseは``カラムです。 
# MAGIC
# MAGIC AutoMLのMetricや実行時間とトライアル回数については、Advance Menuで選択できます。
# MAGIC
# MAGIC Forecast horizon and frequency(予測対象の期間)は`2` ヶ月とします
# MAGIC
# MAGIC Startをクリックすると、あとはDatabricksがやってくれます。
# MAGIC
# MAGIC この作業はUIで行いますが[python API](https://docs.databricks.com/applications/machine-learning/automl.html#automl-python-api-1)による操作も可能です。

# COMMAND ----------

# MAGIC %md ## 実験の経過や結果については、MLflow のExperiment画面で確認可能です。
# MAGIC
# MAGIC <img src='https://github.com/skotani-db/SAP-demand-forecast-on-databricks/blob/main/static/03-machine-learning/experiment.png?raw=true' />

# COMMAND ----------

# MAGIC %md ## 注意事項
# MAGIC
# MAGIC - AutoMLは、シングルノード上で実験が行われるため、メモリサイズが小さいと学習できるデータセット数が小さくなります。そのためメモリ搭載の多いインスタンスを選択してください。 
# MAGIC - 上図(MLflow Experiment UI)の Warningタブを確認ください。
# MAGIC - 以下は一例
# MAGIC
# MAGIC <img src='https://raw.githubusercontent.com/microsoft/openhack-for-lakehouse-japanese/main/images/day2_02__automl/tutoml_alert.png' />

# COMMAND ----------

# MAGIC %md ## AutoMLが完了した後は

# COMMAND ----------

# MAGIC %md 
# MAGIC 表示された結果にチェックボックスをつけて、compareを押してください
# MAGIC <img src='https://github.com/skotani-db/SAP-demand-forecast-on-databricks/blob/main/static/03-machine-learning/compare.png?raw=true' />

# COMMAND ----------

# MAGIC %md ## モデルごとのmetrics比較を行なってください

# COMMAND ----------

# MAGIC %md 
# MAGIC
# MAGIC <img src='https://github.com/skotani-db/SAP-demand-forecast-on-databricks/blob/main/static/03-machine-learning/metrics.png?raw=true' />

# COMMAND ----------

# MAGIC %md ## mlflowから作成したモデルをModel registryに登録
# MAGIC <br>
# MAGIC </br>
# MAGIC <img src='https://raw.githubusercontent.com/microsoft/openhack-for-lakehouse-japanese/main/images/day2_01__mlflow/mlflow-first.png' />
# MAGIC <br>
# MAGIC </br>
# MAGIC
# MAGIC **ご自身のお名前をいれたmodel名にしてください** 
# MAGIC
# MAGIC <img src='https://raw.githubusercontent.com/microsoft/openhack-for-lakehouse-japanese/main/images/day2_01__mlflow/register_model.jpg' />
# MAGIC <br>
# MAGIC </br>
# MAGIC
# MAGIC **赤枠をクリックしてください** 
# MAGIC <img src='https://raw.githubusercontent.com/microsoft/openhack-for-lakehouse-japanese/main/images/day2_01__mlflow/regist_model2.jpg' />
# MAGIC <br>
# MAGIC </br>
# MAGIC
# MAGIC **Transit to productionをクリックします** 
# MAGIC <img src='https://raw.githubusercontent.com/microsoft/openhack-for-lakehouse-japanese/main/images/day2_01__mlflow/mlflow-second.png' />
# MAGIC <br>
# MAGIC </br>
# MAGIC **この作業を実施することで、DatabricksのModel Registryに登録が行われ、mlflowのAPIやsparkから呼び出すことが可能になります。modelの確認はサイドバーからでも確認可能です**
