---
title: "Lab 2: Databricks におけるデータ準備"
weight: 30
---

このラボでは Databricks におけるデータ準備の流れを学びます。
前のラボで S3 に取り込んだ SAP データを Databricks で読み込み、データの前処理を行い、次の機械学習モデル開発のラボで利用するテーブルを作成します。

## 事前準備: Databricks クラスターの作成

データ準備や機械学習モデルの開発は Databricks ノートブック上で行います。
ここでは、バックエンドの計算環境である Databricks クラスターを作成します。

### インスタンスプロファイルの作成

Databricks on AWS のクラスターの実態は Amazon EC2 インスタンスです。
クラスター上で動いているノートブックから S3 バケットをマウントしたり、Amazon ECR のコンテナリポジトリにアクセスしたり、Amazon SageMaker の推論エンドポイントを作成するためには、EC2 に対して必要な権限をまとめた IAM ロールを作成し、アタッチする必要があります。
インスタンスプロファイルは IAM ロールのコンテナであり、インスタンスの起動時に EC2 インスタンスにロール情報を渡すためのコネクターの役割をします。

#### Step 1: インスタンスプロファイルと IAM ロールの作成

インスタンスプロファイルを作成します。

```bash:
aws iam create-instance-profile --instance-profile-name databricks-cluster-sagemaker-access-role
```

IAM ロールを作成します。

```bash:
aws iam create-role --role-name databricks-cluster-sagemaker-access-role --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ec2.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        },
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "sagemaker.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}'
```

IAM ロールをインスタンプロファイルに紐づけます。

```bash
aws iam add-role-to-instance-profile \
  --instance-profile-name databricks-cluster-sagemaker-access-role \
  --role-name databricks-cluster-sagemaker-access-role
```

<!--
#### Step 1: IAM ロールの作成

1. AWS コンソールで、IAM サービスに移動します。
2. サイドバーの「Roles」タブをクリックします。
3. 「Create role」をクリックします。
4. 「Trusted entity type」で「AWS service」を選択します。
5. 「Use case」で「EC2」を選択し、「Next」をクリックします。
![](/static/03-machine-learning/select-trusted-entity.png)
6. 「Add permissions」の画面で「AmazonSageMakerFullAccess」ポリシーを検索し、選択します。
![](/static/03-machine-learning/add-sagemaker-full-access.png)
::alert[ここでは簡単のために広い権限を付与していますが、実際の運用では最小権限の原則に則り、必要な権限だけに絞って付与するようにしてください。]{type=warning}
7. 「Next」をクリックします。
8. 「Role details」の「Role name」に任意の名前を入力します (例: `databricks-cluster-sagemaker-access-role`)。
9. 「Create role」をクリックします。

#### Step 2: 作成した IAM ロールの信頼関係を更新

1. ロール作成後に表示される「View role」ボタンをクリックします。見つからない場合は、ロールの検索バーに作成したロール名を入力し、ロール名のリンクをクリックします。
![](/static/03-machine-learning/view-databricks-cluster-sagemaker-access-role.png)
2. 「Trust relationships」タブを開き、「Edit trust relationship」をクリックします。
3. エディタに以下の JSON をペーストして「Update policy」をクリックします。
```json:
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "ec2.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    },
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "sagemaker.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```
-->

#### Step 2: IAM ロールに AWS マネージドポリシーをアタッチ 

Amazon S3 アクセス権限を追加します。
```bash:
aws iam attach-role-policy --role-name databricks-cluster-sagemaker-access-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
```

Amazon ECR アクセス権限を追加します。
```bash:
aws iam attach-role-policy --role-name databricks-cluster-sagemaker-access-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryFullAccess
```

Amazon SageMaker アクセス権限を追加します。
```bash:
aws iam attach-role-policy --role-name databricks-cluster-sagemaker-access-role \
  --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess
```

Databricks クラスターにインスタンスプロファイルをアタッチする際に必要な権限をインラインポリシーとして追加します。

```bash:
AWS_ACCOUNT_ID=`aws sts get-caller-identity --query "Account" --output text`
cat << EOF > get-role-inline-policy.json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "iam:GetRole"
            ],
            "Resource": [
                "arn:aws:iam::${AWS_ACCOUNT_ID}:role/databricks-cluster-sagemaker-access-role"
            ],
            "Effect": "Allow"
        }
    ]
}
EOF
aws iam put-role-policy \
  --role-name databricks-cluster-sagemaker-access-role \
  --policy-name get-role-inline-policy \
  --policy-document file://get-role-inline-policy.json
```

Databricks ワークスペースの IAM ロール (`databricks-cross-account-role`) に対して、今回作成したロール (`databricks-cluster-sagemaker-access-role`) を渡せる権限を付与します。

```bash:
AWS_ACCOUNT_ID=`aws sts get-caller-identity --query "Account" --output text`
cat << EOF > pass-cluster-role-inline-policy.json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Action": [
                "iam:PassRole"
            ],
            "Resource": [
                "arn:aws:iam::${AWS_ACCOUNT_ID}:role/databricks-cluster-sagemaker-access-role"
            ],
            "Effect": "Allow"
        }
    ]
}
EOF
aws iam put-role-policy \
  --role-name databricks-cross-account-role \
  --policy-name pass-cluster-role-inline-policy \
  --policy-document file://pass-cluster-role-inline-policy.json
```


### Databricks ワークスペースにインスタンスプロファイルを登録

1. Databricks ワークスペースにログインし、右上のユーザー名からメニューを開き、「Admin Settings」をクリックします。
![](/static/02-data-preparation/admin-settings.png)
2. 「Instance profiles」タブの「Add instance profile」ボタンをクリックします。
3. 「Instance profile ARN」に、先ほど作成したインスタンスプロファイルの ARN (`arn:aws:iam::<!!!your-aws-account-id!!!>:instance-profile/databricks-cluster-sagemaker-access-role`) を入力し、他は空のままにして「Add」ボタンをクリックします。

### Databricks クラスターの作成

1. Databricks ワークスペースの左ペインの「Compute」をクリックします。
![](/static/02-data-preparation/compute.png)
2. 「All-purpose compute」タブの「Create compute」ボタンをクリックします。
3. 以下のスクリーンショットを参考に設定し、「Create cluster」ボタンをクリックします。なお、ここでは「Single node」モードを選択し、「Databricks runtime version」は「Runtime: 12.2 LTS **ML** (Scala 2.12, Spark 3.3.2)」を選択し、「Use Photon Acceleration」チェックボックスを外し、「Instance Profile」には「databricks-cluster-sagemaker-access-role」を選択します。
![](/static/02-data-preparation/create-cluster.png)

## Amazon SageMaker 推論コンテナ作成用の環境を構築

ラボ3では、Databricks 上で開発した機械学習モデルを Amazon SageMaker の推論エンドポイントとしてデプロイする手順を解説します。
その際に、推論用コンテナをビルドする必要があります。
手元に Docker 構築環境がない場合は、あらかじめ以下のコマンドで SageMaker Notebook インスタンスを作成しておいてください。

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

## ハンズオン用のノートブック

ハンズオン用のノートブックは `201-data-prep.ja.py` です。

:button[201-data-prep.ja.py]{href="/static/02-data-preparation/notebooks/201-data-prep.ja.py" action=download}

講師が説明する手順に従ってこちらのファイルを Databricks ワークスペースにインポートしてください。

<!--
## Databricks ワークスペースにハンズオン用のノートブックをアップロード

以下のボタンを右クリックしてローカル PC 内に `201-data-prep.ja.py` を保存してください。

:button[201-data-prep.ja.py]{href="/static/02-data-preparation/notebooks/201-data-prep.ja.py" action=download}

1. Databricks ワークスペースの左ペインの「Workspace」をクリックします。
2. 「Home」を右クリックして、「Import」をクリックします。
![](/static/02-data-preparation/import.png)
3. 以下のモーダル画面が表示されるので、灰色の枠内にダウンロードした `201-data-prep.ja.py` をドラッグアンドドロップし、「Import」ボタンをクリックします。
![](/static/02-data-preparation/import-modal.png)
4. 
-->



## 参考文献

- [Set up AWS authentication for SageMaker deployment](https://docs.databricks.com/administration-guide/cloud-configurations/aws/sagemaker.html)
