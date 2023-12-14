---
title: "Lab 2: Databricks におけるデータ準備"
weight: 30
---

このラボでは Databricks におけるデータ準備の流れを学びます。
前のラボで S3 に取り込んだ SAP データを Databricks で読み込み、データの前処理を行い、次の機械学習モデル開発のラボで利用するテーブルを作成します。

## 事前準備: Databricks クラスターの作成と権限付与

データ準備や機械学習モデルの開発は Databricks ノートブック上で行います。
ここでは、バックエンドの計算環境である Databricks クラスターを作成します。

Databricks on AWS のクラスターの実態は Amazon EC2 インスタンスです。
クラスター上で動いているノートブックから S3 バケットをマウントしたり、Amazon ECR のコンテナリポジトリにアクセスしたり、Amazon SageMaker の推論エンドポイントを作成するためには、EC2 に対して必要な権限をまとめた IAM ロールを作成し、アタッチする必要があります。
インスタンスプロファイルは IAM ロールのコンテナであり、インスタンスの起動時に EC2 インスタンスにロール情報を渡すためのコネクターの役割をします。

::::tabs{variant="container"}
:::tab{id="handson" label="ハンズオン用 AWS アカウントを利用する場合"}
ワークショップ用に払い出された AWS アカウントを利用する場合、あらかじめ AWS CloudFormation を用いて IAM 関連のリソースが作成されています。
一部、Databricks のアカウント ID や、Databricks のクイックスタートにより作成されたクロスアカウントロールの設定を追加で行う必要があります。

以下の CLI コマンドをコピーし、AWS CloudShell に貼り付けて実行してください。

```bash:
# Databricks クイックスタートの CloudFormation スタックで作成されたリソースとパラメータを取得
STACK_NAME=`aws cloudformation list-stacks | jq -r '.StackSummaries[] | select(.StackName | startswith("databricks-workspace-stack")) | .StackName'`
DATABRICKS_ROLE_NAME=`aws cloudformation list-stack-resources --stack-name ${STACK_NAME} | jq -r '.StackResourceSummaries[] | select(.LogicalResourceId == "workspaceIamRole") | .PhysicalResourceId'`
DATABRICKS_ACCOUNT_ID=`aws cloudformation describe-stacks --stack-name ${STACK_NAME} | jq -r '.Stacks[0].Parameters[] | select(.ParameterKey == "AccountId") | .ParameterValue'`

echo AWS CloudFormation Stack Name: ${STACK_NAME}
echo Databricks Role Name: ${DATABRICKS_ROLE_NAME}
echo Databricks Account ID: ${DATABRICKS_ACCOUNT_ID}

# 自動で作成済みの databricks-cluster-sagemaker-access-role の Assume Role Policy をアップデート
AWS_ACCOUNT_ID=`aws sts get-caller-identity --query "Account" --output text`
cat << EOF > trust-policy.json
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
        },
        {
            "Effect": "Allow",
            "Principal": {
              "AWS": [
                "arn:aws:iam::414351767826:role/unity-catalog-prod-UCMasterRole-14S5ZJVKOTYTL",
                "arn:aws:iam::${AWS_ACCOUNT_ID}:role/databricks-cluster-sagemaker-access-role"
              ]
            },
            "Action": "sts:AssumeRole",
            "Condition": {
              "StringEquals": {
                "sts:ExternalId": "${DATABRICKS_ACCOUNT_ID}"
              }
            }
        }
    ]
}
EOF
aws iam update-assume-role-policy --role-name databricks-cluster-sagemaker-access-role --policy-document file://trust-policy.json

# Databricks コントロールプレーンが databricks-cluster-sagemaker-access-role をクラスターに付与できるようにする
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
  --role-name ${DATABRICKS_ROLE_NAME} \
  --policy-name pass-cluster-role-inline-policy \
  --policy-document file://pass-cluster-role-inline-policy.json

```
:::
:::tab{id="byoa" label="ご自身の AWS アカウントを利用する場合"}


### インスタンスプロファイルの作成



#### Step 1: インスタンスプロファイルと IAM ロールの作成

インスタンスプロファイルを作成します。AWS CloudShell など、AWS CLI が利用可能な環境で実行してください。

```bash:
aws iam create-instance-profile --instance-profile-name databricks-cluster-sagemaker-access-role
```

[Databricks の管理者コンソール](https://accounts.cloud.databricks.com/)にアクセスし、右上のユーザー名の横にある下矢印をクリックしてください。
ドロップダウンメニューで、アカウント ID (例: 1abc23de-e4ed-56d7-ae89-abc12d345e60) をコピーしてください。
![Check Databricks Account ID](/static/00-prerequisites/databricks-account-id.png)

`<DATABRICKS-ACCOUNT-ID>`を置換し、IAM ロールを作成します。

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
        },
        {
            "Effect": "Allow",
            "Principal": {
              "AWS": [
                "arn:aws:iam::414351767826:role/unity-catalog-prod-UCMasterRole-14S5ZJVKOTYTL"
              ]
            },
            "Action": "sts:AssumeRole",
            "Condition": {
              "StringEquals": {
                "sts:ExternalId": "<DATABRICKS-ACCOUNT-ID>"
              }
            }
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
信頼関係ポリシーを変更して「自己信頼ポリシー」にします。
`<DATABRICKS-ACCOUNT-ID>` の部分は先ほどコピーした Databricks のアカウント ID に置き換えてください。
```bash:
AWS_ACCOUNT_ID=`aws sts get-caller-identity --query "Account" --output text`
cat << EOF > trust-policy.json
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
        },
        {
            "Effect": "Allow",
            "Principal": {
              "AWS": [
                "arn:aws:iam::414351767826:role/unity-catalog-prod-UCMasterRole-14S5ZJVKOTYTL",
                "arn:aws:iam::${AWS_ACCOUNT_ID}:role/databricks-cluster-sagemaker-access-role"
              ]
            },
            "Action": "sts:AssumeRole",
            "Condition": {
              "StringEquals": {
                "sts:ExternalId": "<DATABRICKS-ACCOUNT-ID>"
              }
            }
        }
    ]
}
EOF
aws iam update-assume-role-policy \
  --role-name databricks-cluster-sagemaker-access-role \
  --policy-document file://trust-policy.json --output text
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
  --policy-document file://get-role-inline-policy.json --output text
```

Databricks ワークスペースのクロスアカウントロール (\*) に対して、今回作成したロール (`databricks-cluster-sagemaker-access-role`) を渡せる権限を付与します。
付与先のロール名は、
- 事前準備を [Option 1: クイックスタート](/00-prerequisites/option1-quickstart) で行なった場合は、Databricks アカウントコンソールの Cloud Resources から`databricks-workspace-stack-xxxxx-credentials` をクリックし、「Role Arn」の末尾の IAM Role 名をコピーします。

![Cloud Resources](/static/02-data-preparation/cloud-resouces.png)

![Cross Account Role](/static/02-data-preparation/cross-account-role.png)

- 事前準備を [Option 2: Databricks パートナーアカウント等をお持ちの場合](/00-prerequisites/option2-partner-account) でワークスペースのデプロイを行なった場合は、`databricks-cross-account-role` です。

そして特定した IAM Role 名で以下コマンドの `<YOUR IAM ROLE NAME>` を置換し、コマンドを実行します。

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
  --role-name <YOUR IAM ROLE NAME> \
  --policy-name pass-cluster-role-inline-policy \
  --policy-document file://pass-cluster-role-inline-policy.json
```

:::
::::

### Databricks ワークスペースにインスタンスプロファイルを登録

1. Databricks ワークスペースにログインし、右上のユーザー名からメニューを開き、「Admin Settings」をクリックします。
![Open Databricks Admin Settings](/static/02-data-preparation/admin-settings.png)
<!--2. 「Instance profiles」タブの「Add instance profile」ボタンをクリックします。-->
2. 「Security」メニューの「Instance profiles」欄の「Manage」ボタンをクリックします。
3. 右側の「Add instance profile」ボタンをクリックします。
3. 「Instance profile ARN」に、先ほどセットアップしたインスタンスプロファイルの ARN (`arn:aws:iam::<!!!your-aws-account-id!!!>:instance-profile/databricks-cluster-sagemaker-access-role`) を入力し、他は空のままにして「Add」ボタンをクリックします。

10秒ほど待つとインスタンスプロファイルがワークスペースに登録されます。

### Databricks クラスターの作成

1. Databricks ワークスペースの左ペインの「Compute」をクリックします。

![Compute button](/static/02-data-preparation/compute.png)

2. 「All-purpose compute」タブの「Create compute」ボタンをクリックします。
3. 以下のスクリーンショットを参考に設定し、「Create cluster」ボタンをクリックします。なお、ここでは「Single node」モードを選択し、「Databricks runtime version」は「**Runtime: 13.3 LTS ML (Scala 2.12, Spark 3.4.1)**」を選択し、「Use Photon Acceleration」チェックボックスを外し、「Instance Profile」には「databricks-cluster-sagemaker-access-role」を選択します。

::alert[ランタイムには Standard と ML の2種類がありますが **必ず ML を選んでください**。ML を選ばないとこの先の AutoML や Mlflow を扱うセクションが実行できなくなります。]{type=warning}

![New compute settings](/static/02-data-preparation/create-cluster.png)

数分まつとクラスターが立ち上がります。

::alert[今回は「Single node」モードを選択しましたが、「Multi node」モードを選択すると複数のインスタンスで分散処理し、かつ負荷に応じてオートスケールさせる設定を簡単に行うことができます。]{type=info}

::alert[クラスターの起動中は裏側の EC2 インスタンスが起動中であり、課金対象となります。不用意な請求を防ぐために、使用していないときはクラスターを停止するように気をつけてください。上記の設定 (Terminate after 120 minutes of inactivity) では、クラスターが120分間アイドル状態となると自動的に停止します。]{type=warning}

## Databricks ワークスペースにハンズオン用のノートブックをダウンロード

ハンズオン用のノートブックとファイルは以下の GitHub リポジトリの `assets` ディレクトリに格納されています。
```
https://github.com/skotani-db/SAP-demand-forecast-on-databricks.git
```

1. Databricks ワークスペースの左ペインの「Workspace」をクリックします。
2. 「Repos」を選択し、右側の「Add repo」をクリックします。

![File import](/static/02-data-preparation/add_repo.png)

3. 以下のモーダル画面が表示されるので、"Git repository URL" に `https://github.com/skotani-db/SAP-demand-forecast-on-databricks.git` と入力し、「Create Repo」ボタンをクリックします。

![Import modal](/static/02-data-preparation/create-repo.png)

無事インポートできたらファイルエクスプローラーにリポジトリ内のファイルが表示されます。
`assets` ディレクトリをクリックし、`201-data-prep.ja` ノートブックを開き、ノートブック内に記載されている手順に沿って進めてください。

## 参考文献

- [Set up AWS authentication for SageMaker deployment](https://docs.databricks.com/administration-guide/cloud-configurations/aws/sagemaker.html)

::alert[ご自身の AWS アカウントを利用している場合、途中でラボを退出すると意図せず課金が継続される可能性があります。中断する場合は [あと片付け](/09-clearnup) の手順に従い、不要なリソースを削除するよう気をつけてください。]{type=warning}
