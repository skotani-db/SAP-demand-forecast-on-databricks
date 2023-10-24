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

インスタンスプロファイルを作成します。AWS CloudShell など、AWS CLI が利用可能な環境で実行してください。

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

Amazon S3 アクセス権限を追加します。AWS CloudShell など、AWS CLI が利用可能な環境で実行してください。
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
![Open Databricks Admin Settings](/static/02-data-preparation/admin-settings.png)
2. 「Instance profiles」タブの「Add instance profile」ボタンをクリックします。
3. 「Instance profile ARN」に、先ほど作成したインスタンスプロファイルの ARN (`arn:aws:iam::<!!!your-aws-account-id!!!>:instance-profile/databricks-cluster-sagemaker-access-role`) を入力し、他は空のままにして「Add」ボタンをクリックします。

### Databricks クラスターの作成

1. Databricks ワークスペースの左ペインの「Compute」をクリックします。
![Compute button](/static/02-data-preparation/compute.png)
2. 「All-purpose compute」タブの「Create compute」ボタンをクリックします。
3. 以下のスクリーンショットを参考に設定し、「Create cluster」ボタンをクリックします。なお、ここでは「Single node」モードを選択し、「Databricks runtime version」は「**Runtime: 13.3 LTS ML (Scala 2.12, Spark 3.4.1)**」を選択し、「Use Photon Acceleration」チェックボックスを外し、「Instance Profile」には「databricks-cluster-sagemaker-access-role」を選択します。
![New compute settings](/static/02-data-preparation/create-cluster.png)

::alert[今回は「Single node」モードを選択しましたが、「Multi node」モードを選択すると複数のインスタンスで分散処理し、かつ負荷に応じてオートスケールさせる設定を簡単に行うことができます。]{type=info}

::alert[クラスターの起動中は裏側の EC2 インスタンスが起動中であり、課金対象となります。不用意な請求を防ぐために、使用していないときはクラスターを停止するように気をつけてください。上記の設定 (Terminate after 120 minutes of inactivity) では、クラスターが120分間アイドル状態となると自動的に停止します。]{type=warning}

## ハンズオン用のノートブックとファイル

ハンズオン用のノートブックは `201-data-prep.ja.py` です。
以下のボタンを右クリックしてローカル PC 内に `201-data-prep.ja.py` を保存してください。

:button[201-data-prep.ja.py]{href="/static/02-data-preparation/notebooks/201-data-prep.ja.py" action=download}

また、ハンズオンで用いる CSV ファイルも併せて保存してください。

:button[vbak_mapping.csv]{href="/static/02-data-preparation/notebooks/vbak_mapping.csv" action=download}
:button[vbap_mapping.csv]{href="/static/02-data-preparation/notebooks/vbap_mapping.csv" action=download}

## Databricks ワークスペースにハンズオン用のノートブックをアップロード

1. Databricks ワークスペースの左ペインの「Workspace」をクリックします。
2. 「Home」を選択した状態で右側にある縦三点リーダーをクリックし、「Import」をクリックします。
![File import](/static/02-data-preparation/file-import.png)
3. 以下のモーダル画面が表示されるので、灰色の枠内にダウンロードした `201-data-prep.ja.py`、`vbak_mapping.csv`、`vbap_mapping.csv` をドラッグアンドドロップし、「Import」ボタンをクリックします。
![Import modal](/static/02-data-preparation/import-modal.png)

無事インポートできたらファイルエクスプローラーに `201-data-prep.ja` のリンクが表示されます。
そちらのリンクをクリックし、ノートブックを開き、ノートブック内に記載されている手順に沿って進めてください。

## 参考文献

- [Set up AWS authentication for SageMaker deployment](https://docs.databricks.com/administration-guide/cloud-configurations/aws/sagemaker.html)

::alert[ご自身の AWS アカウントを利用している場合、途中でラボを退出すると意図せず課金が継続される可能性があります。中断する場合は [あと片付け](/09-clearnup) の手順に従い、不要なリソースを削除するよう気をつけてください。]{type=warning}
