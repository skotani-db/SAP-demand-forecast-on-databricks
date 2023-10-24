---
title: "MLflow Model Registry から Amazon SageMaker にデプロイ"
weight: 41
---

このラボでは、MLflow のモデルを Amazon SageMaker にデプロイする方法を学びます。

::alert[本ラボを実施するには、[Lab 3: Databricks と MLflow を用いた需要予測モデル開発](/03-machine-learning) の事前準備のセクションにある、mlflow モデルをデプロイ用のコンテナ作成ステップを完了している必要があります。]{type=warning}

ハンズオン用のノートブックは `303-deploy-on-sagemaker.ja.py` です。
以下のボタンを右クリックしてローカル PC 内に `303-deploy-on-sagemaker.ja.py` を保存してください。

:button[303-deploy-on-sagemaker.ja.py]{href="/static/03-machine-learning/notebooks/303-deploy-on-sagemaker.ja.py" action=download}


## Databricks ワークスペースにハンズオン用のノートブックをアップロード

1. Databricks ワークスペースの左ペインの「Workspace」をクリックします。
2. 「Home」を選択した状態で右側にある縦三点リーダーをクリックし、「Import」をクリックします。
![File import](/static/02-data-preparation/file-import.png)
3. 以下のモーダル画面が表示されるので、灰色の枠内にダウンロードした `303-deploy-on-sagemaker.ja.py` をドラッグアンドドロップし、「Import」ボタンをクリックします。
![Import modal](/static/02-data-preparation/import-modal.png)

無事インポートできたらファイルエクスプローラーに `303-deploy-on-sagemaker.ja` のリンクが表示されます。
そちらのリンクをクリックし、ノートブックを開き、ノートブック内に記載されている手順に沿って進めてください。
