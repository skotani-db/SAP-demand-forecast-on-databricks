# Databricks notebook source
# MAGIC %md
# MAGIC # MLflow Model Registry から Amazon SageMaker にデプロイ

# COMMAND ----------

# MAGIC %md
# MAGIC MLflow Model Registry に登録して Production に遷移させたモデルの URI や、Amazon ECR のコンテナリポジトリの URL を変数に格納します。

# COMMAND ----------

region = "us-east-1"
model_uri = "models:/sales-forecast/1"
image_ecr_url = "895319637341.dkr.ecr.us-east-1.amazonaws.com/mlflow-pyfunc:2.1.1"

# COMMAND ----------

# MAGIC %md
# MAGIC `mlflow.deployments` モジュールを用いて SageMaker でのデプロイ用のクライアントを取得します。｀create_deployment` メソッドを実行することで SageMaker のデプロイが始まります。`SageMakerDeploymentClient` の API リファレンスは[こちら](https://mlflow.org/docs/latest/python_api/mlflow.sagemaker.html)です。
# MAGIC
# MAGIC **残念ながら Prophet 自体の問題 (Prophet が依存している holidays ライブラリの仕様変更) で、エンドポイント起動時に Prophet がインポートできず、デプロイに失敗します。**
# MAGIC https://github.com/facebook/prophet/issues/2432

# COMMAND ----------

import mlflow.deployments
 
deployment_name = "sales-forecast-endpoint"
 
deployment_client = mlflow.deployments.get_deploy_client("sagemaker:/" + region)
deployment_client.create_deployment(
    name=deployment_name,
    model_uri=model_uri,
    config={
      "image_url": image_ecr_url
    }
)

# COMMAND ----------

deployment_info = deployment_client.get_deployment(name=deployment_name)
print(f"MLflow SageMaker Deployment status is: {deployment_info['EndpointStatus']}")

# COMMAND ----------


