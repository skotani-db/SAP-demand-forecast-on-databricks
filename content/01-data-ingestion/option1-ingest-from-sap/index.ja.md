---
title: "Option 1: Amazon AppFlow OData Connector を使用して SAP からデータを抽出する"
weight: 21
---

## 1.1 アーキテクチャー

このステップでは、Amazon AppFlow を設定して、OData を通じて SAP S/4HANA から以下のデータを抽出し、Parquet ファイルとして Amazon S3 バケットに保存します。

- 販売伝票ヘッダー
- 販売伝票明細

ワークショップに使用する SAP S/4HANA デモシステムや必要な OData サービスは既に設定してあります。
SAP S/4HANA システムは Private Subnet に配置し、Internet 向けの Application Load Balancer (ALB) 経由でアクセスされるように設定しています。
Amazon AppFlow からこの Internet 向けの ALB 経由で SAP S/4HANA に接続させ、データ抽出フローを設定する作業をワークショップで行います。

::alert[接続先の SAP システムのログイン情報はワークショップ中にお伝えします。ログイン情報が与えられない場合は [Option 2: 公開 S3 バケットから直接 Databricks にデータを取り込む](/09-end-to-end-workshop/01-data-ingestion/option2-ingest-from-s3) の手順に従ってください。]{type=warning}

::alert[ワークショップのために Public ALB で設定していますが、実際大切な業務データを更にセキュアに転送できるように Internal 向けの NLB と AWS Private Link (VPC Endpoint Service) を設定し、プライベートリンク経由の抽出も可能です。]{type=info}
![Arhitecture for data ingestion](/static/01-data-ingestion/option1-ingest-from-sap/index-image001.ja.png)

## アジェンダ

::children