# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC ## Databricks Auto ML と `sales_history` テーブルの使用
# MAGIC
# MAGIC <img style="float: right" width="600" src='https://github.com/skotani-db/SAP-demand-forecast-on-databricks/blob/main/static/03-machine-learning/automl-setting.png?raw=true'>
# MAGIC
# MAGIC Auto ML は、「Machine Learning (機械学習)」メニュースペースで利用できます。<br>
# MAGIC (左ペインの Machine Learning セクションの下にある Experiments を選択してください。)
# MAGIC
# MAGIC 「Create AutoML Experiment」ボタンをクリックして新規に Auto-ML 実験を開始し、先ほど作成した特徴量テーブル(`default.sales_history`) を選択するだけで自動的にモデルが学習されます。
# MAGIC
# MAGIC ML Problem type は、今回は `Forcasting` です。 \
# MAGIC prediction target は `Price` カラムです。 \
# MAGIC Time column は `YearMonth` カラムです。 \
# MAGIC Output Database は `default` です。 
# MAGIC
# MAGIC Forecast horizon and frequency (予測対象の期間)は `2` ヶ月とします
# MAGIC
# MAGIC AutoML の Metric や実行時間とトライアル回数については、「Advance Menu (optional)」で選択できます。
# MAGIC
# MAGIC 今回は「Timeout (minutes)」を `5` 分などにして時間短縮してください。
# MAGIC
# MAGIC Start をクリックすると、あとは Databricks がやってくれます。
# MAGIC
# MAGIC この作業は UI で行いますが [python API](https://docs.databricks.com/applications/machine-learning/automl.html#automl-python-api-1) による操作も可能です。

# COMMAND ----------

# MAGIC %md ## 実験の経過や結果については、MLflow の Experiment 画面で確認可能です。
# MAGIC
# MAGIC 時間が経っても実験結果が確認できない場合は画面右端の更新アイコンをクリックしてください。
# MAGIC
# MAGIC <img src='https://github.com/skotani-db/SAP-demand-forecast-on-databricks/blob/main/static/03-machine-learning/experiment.png?raw=true' />

# COMMAND ----------

# MAGIC %md ## 注意事項
# MAGIC
# MAGIC - AutoML は、シングルノード上で実験が行われるため、メモリサイズが小さいと学習できるデータセット数が小さくなります。そのためメモリ搭載の多いインスタンスを選択してください。 
# MAGIC - 上図 (MLflow Experiment UI) の Warning タブを確認ください。
# MAGIC - 以下は一例
# MAGIC
# MAGIC <img src='https://raw.githubusercontent.com/microsoft/openhack-for-lakehouse-japanese/main/images/day2_02__automl/tutoml_alert.png' />

# COMMAND ----------

# MAGIC %md ## AutoML が完了した後は

# COMMAND ----------

# MAGIC %md 
# MAGIC 表示された結果にチェックボックスをつけて、compareを押してください
# MAGIC <img src='https://github.com/skotani-db/SAP-demand-forecast-on-databricks/blob/main/static/03-machine-learning/compare.png?raw=true' />

# COMMAND ----------

# MAGIC %md ## モデルごとの metrics 比較を行なってください

# COMMAND ----------

# MAGIC %md 
# MAGIC
# MAGIC <img src='https://github.com/skotani-db/SAP-demand-forecast-on-databricks/blob/main/static/03-machine-learning/metrics.png?raw=true' />

# COMMAND ----------

# MAGIC %md ## 作成したモデルを MLflow Model Registry に登録
# MAGIC
# MAGIC 最もスコアが良かった Run を開き、学習したモデルを Model Registry に登録していきます。
# MAGIC <br>
# MAGIC </br>
# MAGIC <img src='https://raw.githubusercontent.com/microsoft/openhack-for-lakehouse-japanese/main/images/day2_01__mlflow/mlflow-first.png' />
# MAGIC <br>
# MAGIC </br>
# MAGIC
# MAGIC **ご自身のお名前をいれた model 名にしてください** 
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
# MAGIC **Transit to production をクリックします** 
# MAGIC <img src='https://raw.githubusercontent.com/microsoft/openhack-for-lakehouse-japanese/main/images/day2_01__mlflow/mlflow-second.png' />
# MAGIC <br>
# MAGIC </br>
# MAGIC **この作業を実施することで、Databricks の Model Registry に登録が行われ、mlflow の API や spark から呼び出すことが可能になります。model の詳細はサイドバーの「Models」からでも確認可能です**

# COMMAND ----------

# MAGIC %md ## 予測と実績を確認するためのデータマートを作成
# MAGIC
# MAGIC 「Lab 4: 可視化ダッシュボード開発」で利用する、実績と予測を組み合わせたテーブルを作成します。

# COMMAND ----------

# 予測テーブルの特定
forecast_table_name = (
                        spark
                        .sql("SHOW TABLES")
                        .filter("tableName like 'forecast_prediction_%'")
                        .select("tableName")
                        .collect()[0][0]
                        )

display(forecast_table_name)

# COMMAND ----------

# 実績と予測を組み合わせる
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
# MAGIC これで機械学習モデルの開発およびデータマートの作成は完了です。
# MAGIC
# MAGIC ワークショップページに戻り「MLflow Model Registry から Amazon SageMaker にデプロイ」のセクションに進むか、もしくは「Lab 4: 可視化ダッシュボード開発」に進んでください。

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
