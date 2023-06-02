---
title: "End-to-End Workshop"
weight: 0
---

## SAP データを用いた Databricks on AWS における需要予測ワークショップ

本ワークショップでは Databricks と AWS サービスとの連携方法を学びます。具体的には、SAP 上のデータを Amazon AppFlow で Amazon S3 に取り込み、Databricks 上で ETL、機械学習モデルの作成、予測、Amazon QuickSight 上でのダッシュボード作成、Amazon SageMaker でのモデルデプロイの手順を体験いただきます。
本ワークショップは、主に Databricks のユーザーペルソナでもあるデータエンジニアや、データサイエンティストや、データアナリストを対象としていますが、SAP on AWS 上のデータ活用方法について学びたい方や、Databricks と AWS サービスをどのようにして連携したいか知りたい方にもおすすめです。

## ワークショップの概要

1. SAP >> AWS (Amazon S3) データ取り込み
  * [Option 1] Amazon AppFlow 経由で S3 にコピー 
  * [Option 2] S3 バケットからデータをコピー
2. Databricks on AWS でデータ準備
  1. PySpark で Silver、Gold テーブル作成 
    * テーブルの結合・クレンジング、機械学習用にデータの整形
  2. Delta Live Table として ETL ワークフロー化
3. Databricks on AWS で機械学習モデルを開発
  1. (需要予測) 機械学習モデルを開発
  2. MLflow Model Registry に登録
  3. Amazon SageMaker のリアルタイム推論エンドポイントとしてデプロイ
4. データ可視化ダッシュボード作成
  * [Option 1] Databricks SQL 利用
  * [Option 2] Amazon QuickSight 利用

これらのワークショップの実行には手順が詳しく説明されているので、AWS や Databricks の知識は必要ありません。
ワークショップ全体の所要時間は約2時間です。



