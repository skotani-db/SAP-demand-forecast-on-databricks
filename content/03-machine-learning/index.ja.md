---
title: "Lab 3: Databricks と MLflow を用いた需要予測モデル開発"
weight: 40
---

このラボでは Databricks 上で機械学習モデルの開発を行う手順を解説します。
`301-eda.ja.py` のノートブックでは、データの理解のための探索的データ分析 (EDA) を行い、`302-machine-learning.ja.py` のノートブックでは、Databricks AutoML を用いて機械学習モデルを開発し、次のダッシュボード開発で用いる予測結果を含んだテーブルを作成します。

以下のボタンを右クリックしてローカル PC 内に `301-eda.ja.py`、`302-machine-learning.ja.py` を保存してください。

:button[301-eda.ja.py]{href="/static/03-machine-learning/notebooks/301-eda.ja.py" action=download}
:button[302-machine-learning.ja.py]{href="/static/03-machine-learning/notebooks/302-machine-learning.ja.py" action=download}

## Databricks ワークスペースにハンズオン用のノートブックをアップロード

1. Databricks ワークスペースの左ペインの「Workspace」をクリックします。
2. 「Home」を選択した状態で右側にある縦三点リーダーをクリックし、「Import」をクリックします。
![File import](/static/02-data-preparation/file-import.png)
3. 以下のモーダル画面が表示されるので、灰色の枠内にダウンロードした `301-eda.ja.py`、`302-machine-learning.ja.py` をドラッグアンドドロップし、「Import」ボタンをクリックします。
![Import modal](/static/02-data-preparation/import-modal.png)

無事インポートできたらファイルエクスプローラーにノートブックを開くためのリンクが表示されます。
まずは、`301-eda.ja.py` のリンクをクリックし、ノートブックを開き、ノートブック内に記載されている手順に沿って進めてください。

------------

また、開発した機械学習モデルを Amazon SageMaker でデプロイする手順についても以下のラボで解説します。

::children

## 事前準備: Amazon SageMaker 推論コンテナ作成用の環境を構築

ラボ3の後半では、Databricks 上で開発した機械学習モデルを Amazon SageMaker の推論エンドポイントとしてデプロイする手順を解説します。
その際に、推論用コンテナをビルドする必要があります。
手元に Docker 構築環境がない場合は、あらかじめ以下のコマンドで SageMaker ノートブックインスタンスを作成しておいてください。

```bash:
AWS_ACCOUNT_ID=`aws sts get-caller-identity --query "Account" --output text`
aws sagemaker create-notebook-instance \
  --notebook-instance-name databricks-on-aws-immersion-day \
  --instance-type ml.t3.large \
  --role-arn arn:aws:iam::${AWS_ACCOUNT_ID}:role/databricks-cluster-sagemaker-access-role \
  --volume-size-in-gb 30 \
  --region us-east-1 \
  --platform-identifier notebook-al2-v2 
```

::alert[SageMaker ノートブックインスタンスが起動している間は課金対象となります。必要がなくなったら [あと片付け](/09-cleanup) の手順を参考にリソースを削除してください。]{type=warning}

## 事前準備: mlflow モデルを SageMaker にデプロイする際に用いるコンテナを作成

1. SageMaker ノートブックインスタンスの作成が完了したら、インスタンスへのログイン用の署名付き URL を取得してください。
```bash:
aws sagemaker create-presigned-notebook-instance-url \
  --notebook-instance-name databricks-on-aws-immersion-day \
  --region us-east-1 \
  --output text
```
::alert[バージニア北部以外のリージョンで作業している場合は `us-east-1` を適宜置き換えてください。]{type=info}
2. 出力された URL を正確にコピーし、ウェブブラウザの URL バーに貼り付けてください。
3. Jupyter の画面が開いたら、「Files」→「New」→「Terminal」から端末を開きます。
![Open terminal](/static/03-machine-learning/open-terminal.png)
4. Databricks クラスターにインストールされているものと同じバージョンの mlflow をインストールします。
```bash:
pip install mlflow==2.5.0
```
5. mlflow に登録されたモデル用の推論コンテナをビルドし、Amazon Elastic Container Registry (Amazon ECR) のリポジトリに登録します。この工程は以下のコマンドで自動的に実行されます。
```bash:
mlflow sagemaker build-and-push-container
```

::alert[コンテナのビルドには20-30分程度かかります。]{type=info}

::alert[ご自身の AWS アカウントを利用している場合、途中でラボを退出すると意図せず課金が継続される可能性があります。中断する場合は [あと片付け](/09-clearnup) の手順に従い、不要なリソースを削除するよう気をつけてください。]{type=warning}