---
title: "あと片付け"
weight: 90
---

## Databricks ワークスペースの削除

Databricks 関連では以下のリソースが課金対象となります。

- Databricks クラスターが稼働する Amazon EC2 インスタンス
- Databricks ワークスペースが稼働する VPC 内のリソース (NAT Gateway 等)
- Databricks 用 Amazon S3 バケット

Databricks クラスターに関してはドキュメント ([Manage clusters](https://docs.databricks.com/en/clusters/clusters-manage.html#terminate-a-cluster)) を参考にして削除してください。

その後、ドキュメント ([Delete a workspace](https://docs.databricks.com/en/administration-guide/workspace/delete-workspace.html)) を参考に、Databricks 管理コンソールよりワークスペースを削除してください。
この操作により VPC リソースなども削除されます。

Databricks 用の S3 バケットに関しては以下のコマンドで削除することができます。
バケット名とリージョン名は適宜置き換えてください。

```bash:
BUCKET_NAME=databricks-root-storage-<!!!your-name!!!>
REGION=us-east-1
# バケットの中身を削除
aws s3 rm s3://${BUCKET_NAME} --recursive --region ${REGION}
# バケット自体を削除
aws s3 rb s3://${BUCKET_NAME} --region ${REGION}
```

::alert[Databricks のサブスクリプション自体をキャンセルする際は Databricks のドキュメント ([Manage your subscription](https://docs.databricks.com/en/administration-guide/account-settings/account.html#cancel-your-databricks-subscription)) を参考にしてください。]{type=info}

## SageMaker ノートブックインスタンスの削除

ラボ3で作成した SageMaker ノートブックインスタンスを削除します。

まずは、以下のコマンドでノートブックインスタンスを停止してください。
インスタンス名やリージョン名は適宜置き換えてください。

```bash:
aws sagemaker stop-notebook-instance --notebook-instance-name databricks-on-aws-immersion-day --region us-east-1
```

インスタンスが停止したら、次に、インスタンスを削除してください。

```bash:
aws sagemaker delete-notebook-instance --notebook-instance-name databricks-on-aws-immersion-day --region us-east-1
```

## Amazon QuickSight ダッシュボードの削除

Amazon QuickSight はサブスクリプションを削除することで裏側のリソースを含めて解放することが可能です。

```bash:
AWS_ACCOUNT_ID=`aws sts get-caller-identity --query "Account" --output text`
aws quicksight delete-acount-subscription --aws-acount-id ${AWS_ACCOUNT_ID} --region us-east-1
```

::alert[QuickSight のサブスクリプションを維持しつつ本ワークショップで作成したリソースのみを削除したい場合は [Deleting datasets](https://docs.aws.amazon.com/quicksight/latest/user/delete-a-data-set.html) や [Deleting an analysys](https://docs.aws.amazon.com/quicksight/latest/user/deleting-an-analysis.html) の手順を参考にしてください。]{type=warning}

## Amazon AppFlow のデータ送信先 S3 バケットの削除

SAP から Amazon AppFlow でデータを抽出する際の保存先として作成した S3 バケットを削除します。
バケット名が `111122223333-appflowodata-20230829` のような形式でない場合は適宜コマンド (`BUCKET_NAME` の部分) を書き換えてください。

```bash:
AWS_ACCOUNT_ID=`aws sts get-caller-identity --query "Account" --output text`
BUCKET_NAME=${AWS_ACCOUNT_ID}-appflowodata-`date "+%Y%m%d"`
REGION=us-east-1
# バケットの中身を削除
aws s3 rm s3://${BUCKET_NAME} --recursive --region ${REGION}
# バケット自体を削除
aws s3 rb s3://${BUCKET_NAME} --region ${REGION}
```

## Amazon Elastic Container Registry のリポジトリの削除

mlflow モデルのデプロイ用に作成したコンテナイメージが登録された ECR リポジトリは以下のコマンドで削除します。

```bash:
aws ecr delete-repository \
    --repository-name mlflow-pyfunc \
    --region us-east-1 \
    --force 
```

## (Optional) その他リソースの削除

その他のリソースに料金は発生しませんが、削除したい場合は以下のドキュメントを参考にしてください。

- [ロールまたはインスタンスプロファイルの削除](https://docs.aws.amazon.com/ja_jp/IAM/latest/UserGuide/id_roles_manage_delete.html)
- [Managing Amazon AppFlow Connections](https://docs.aws.amazon.com/ja_jp/appflow/latest/userguide/connections.html)
- [Managing flows](https://docs.aws.amazon.com/ja_jp/appflow/latest/userguide/flows-manage.html)
