---
title: "MLflow Model Registry から Amazon SageMaker にデプロイ"
weight: 41
---

このラボでは、MLflow のモデルを Amazon SageMaker にデプロイする方法を学びます。

## 事前準備: mlflow モデルを SageMaker にデプロイする際に用いるコンテナを作成

1. 事前にラボ 2 で SageMaker Notebook インスタンスを作成した場合は、インスタンスへのログイン用の署名付き URL を取得してください。
```bash:
aws sagemaker create-presigned-notebook-instance-url \
  --notebook-instance-name databricks-on-aws-immersion-day \
  --output text
```
2. 出力された URL を正確にコピーし、ウェブブラウザの URL バーに貼り付けてください。
3. Jupyter の画面が開いたら、「Files」→「New」→「Terminal」から端末を開きます。
![](/static/03-machine-learning/open-terminal.png)
4. Databricks クラスターにインストールされているものと同じバージョンの mlflow をインストールします。
```bash:
pip install mlflow==2.1.1
```
5. mlflow に登録されたモデル用の推論コンテナをビルドし、Amazon ECR のリポジトリに登録します。この工程は以下のコマンドで自動的に実行されます。
```bash:
mlflow sagemaker build-and-push-container
```

::alert[コンテナのビルドには20-30分程度かかります。先にラボ4を実施し、完了後に戻ってきてもよいでしょう。]{type=info}

コンテナのビルドが完了したら Databricks ワークスペースに戻り `303-deploy-on-sagemaker.ja.py` ノートブックを開いてください。
