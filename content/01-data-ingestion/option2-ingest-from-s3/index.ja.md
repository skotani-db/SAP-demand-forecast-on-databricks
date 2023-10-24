---
title: "Option 2: 公開 S3 バケットから直接 Databricks にデータを取り込む"
weight: 22
---

こちらの手順では、AWS が所有している公開 S3 バケットに置いてある SAP サンプルデータをご自身の S3 バケットにコピーします。

## S3 バケットの作成

まずはコピー先の S3 バケットを作成します。
次のコマンドを実行すると `111122223333-appflowodata-20230808` のような名前のバケットがバージニア北部 (us-east-1) リージョンに作成されます。

```bash:
AWS_ACCOUNT_ID=`aws sts get-caller-identity --query "Account" --output text`
MY_BUCKET_NAME=${AWS_ACCOUNT_ID}-appflowodata-`date +%Y%m%d`
aws s3 mb s3://${MY_BUCKET_NAME} --region us-east-1
```

::alert[バージニア北部以外のリージョンで作業している場合は `us-east-1` を適宜置き換えてください]{type=info}
## 公開バケットからのデータのコピー

次に、AWS が所有している公開 S3 バケットにあるデータを、前のステップで作成したバケットにコピーします。
ディレクトリ構造は [Option 1: Amazon AppFlow OData Connector を使用して SAP からデータを抽出する](/09-end-to-end-workshop/01-data-ingestion/option1-ingest-from-sap) の手順で Amazon AppFlow により作成されるものと同等の構成になっています。

```bash:
SALES_HEADER_DIR=salesheader/b44d21c2-118c-4e2f-9d84-37036ff7afd5
SALES_ITEM_DIR=salesitem/4e144a13-7bc0-45d8-a970-85110212f7b3
aws s3 cp s3://machine-learning-contents-aws-jp/databricks-on-aws-immersion-day/${SALES_HEADER_DIR}/1202437098-2023-06-06T07:36:27 s3://${MY_BUCKET_NAME}/${SALES_HEADER_DIR}/
aws s3 cp s3://machine-learning-contents-aws-jp/databricks-on-aws-immersion-day/${SALES_ITEM_DIR}/-1628612112-2023-06-06T07:38:28 s3://${MY_BUCKET_NAME}/${SALES_ITEM_DIR}/
```

