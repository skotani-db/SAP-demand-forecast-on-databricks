# Databricks notebook source
# MAGIC %md
# MAGIC # MLflow Model Registry から Amazon SageMaker にデプロイ

# COMMAND ----------

# MAGIC %md
# MAGIC MLflow Model Registry に登録して Production に遷移させたモデルの URI や、Amazon ECR のコンテナリポジトリの URL を変数に格納します。

# COMMAND ----------

# MAGIC %pip install boto3 -q

# COMMAND ----------

import boto3

account_id = boto3.client("sts").get_caller_identity().get("Account")

# リージョン名は必要に応じて変更
region = "us-east-1"
# Model Registry に登録したモデル名に書き換えてください！
model_uri = "models:/sales-predict/1"
# mlflow sagemaker build-and-push-container コマンドで作成したコンテナイメージ
image_ecr_url = f"{account_id}.dkr.ecr.{region}.amazonaws.com/mlflow-pyfunc:2.5.0"

# COMMAND ----------

# MAGIC %md
# MAGIC `mlflow.deployments` モジュールを用いて SageMaker でのデプロイ用のクライアントを取得します。`create_deployment` メソッドを実行することで SageMaker 推論エンドポイントのデプロイが始まります。`SageMakerDeploymentClient` の API リファレンスは[こちら](https://mlflow.org/docs/latest/python_api/mlflow.sagemaker.html)です。
# MAGIC
# MAGIC > 今回はインスタンス数を `1`、インスタンスタイプを `ml.m4.xlarge` に指定してデプロイしています。インスタンス数を2つ以上にすることで複数の Availability Zone (AZ) に自動的に分散して配置され、推論エンドポイントの可用性を向上することができます。本番運用する際には複数 AZ の構成を取ることが推奨されています。また、SageMaker のリアルタイム推論エンドポイントでは負荷やあらかじめ設定したタイミングに応じたオートスケーリングの設定を行うことができます。詳しくはドキュメントの "[Automatically Scale Amazon SageMaker Modesl](https://docs.aws.amazon.com/sagemaker/latest/dg/endpoint-auto-scaling.html)" を参照してください。

# COMMAND ----------

import mlflow.deployments
 
deployment_name = "sales-predict-endpoint"
 
deployment_client = mlflow.deployments.get_deploy_client("sagemaker:/" + region)
deployment_client.create_deployment(
    name=deployment_name,
    model_uri=model_uri,
    config={
      "image_url": image_ecr_url,
      "instance_count": 1,
      "instance_type": "ml.m4.xlarge",
    }
)

# COMMAND ----------

deployment_info = deployment_client.get_deployment(name=deployment_name)
print(f"MLflow SageMaker Deployment status is: {deployment_info['EndpointStatus']}")

# COMMAND ----------

# MAGIC %md
# MAGIC 推論エンドポイントのデプロイが完了したら、ワークショップページに戻り、次の「Lab 4: 可視化ダッシュボード開発」に進んでください。

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
