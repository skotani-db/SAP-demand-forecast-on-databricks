---
title: "2. (Option 2) Databricks クイックスタートを選択できない場合"
weight: 12
---

::alert[本ワークショップを実行するには Databricks の管理者アカウントおよび AWS アカウントの管理者権限が必要です。Databricks の管理者アカウントをお持ちでない場合は[Option 1: クイックスタート](/00-prerequisites/option1-quickstart)のラボに進んでください。]{type=warning}

::alert[このラボは、Databricks のアカウントの制約上、ワークスペース作成時にクイックスタートのオプションを選択できない方を対象としています。通常のアカウントをお持ちの方は[Option 1: クイックスタート](/00-prerequisites/option1-quickstart)のラボに進んでください。]{type=warning}

### Databricks ワークスペースをデプロイするための IAM ロールを作成

まずは、皆様の AWS アカウントと Databricks の所有するアカウントとを繋ぐクロスアカウントロールを作成します。

1. [Databricks の管理者コンソール](https://accounts.cloud.databricks.com/)にアクセスし、右上のユーザー名の横にある下矢印をクリックしてください。
2. ドロップダウンメニューで、アカウント ID (例: 1abc23de-e4ed-56d7-ae89-abc12d345e60) をコピーしてください。
![Check Databricks Account ID](/static/00-prerequisites/databricks-account-id.png)
3. AWS CloudShell など、AWS CLI がセットアップされた端末に以下のコマンドをコピーし、`<!!!databricks-account-id!!!>` の部分を (2) でコピーしたアカウント ID に書き換えた上で実行してください。
```bash:
aws iam create-role --role-name databricks-cross-account-role --assume-role-policy-document '{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "AWS": "arn:aws:iam::414351767826:root"
            },
            "Action": "sts:AssumeRole",
            "Condition": {
                "StringEquals": {
                    "sts:ExternalId": "<!!!databricks-account-id!!!>"
                }
            }
        }
    ]
}'
```
::alert[`414351767826` は Databricks が所有する AWS アカウントの ID 番号です。ここでは、Databricks のサービスが皆様の AWS アカウント上でリソースをプロビジョニングできるよう、クロスアカウントアクセスの設定を行なっています。所属する組織のポリシーにより、ご自身の環境でクロスアカウントアクセスの設定が許可されているか確認してください。]
4. 以下のコマンドを実行し、作成した IAM ロールに対して Databricks が必要とする権限をまとめたインラインポリシーをセットします。
```bash:
aws iam put-role-policy \
  --role-name databricks-cross-account-role \
  --policy-name databricks-default-deployment-inline-policy \
  --policy-document \
'{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "Stmt1403287045000",
      "Effect": "Allow",
      "Action": [
        "ec2:AllocateAddress",
        "ec2:AssignPrivateIpAddresses",
        "ec2:AssociateDhcpOptions",
        "ec2:AssociateIamInstanceProfile",
        "ec2:AssociateRouteTable",
        "ec2:AttachInternetGateway",
        "ec2:AttachVolume",
        "ec2:AuthorizeSecurityGroupEgress",
        "ec2:AuthorizeSecurityGroupIngress",
        "ec2:CancelSpotInstanceRequests",
        "ec2:CreateDhcpOptions",
        "ec2:CreateFleet",
        "ec2:CreateInternetGateway",
        "ec2:CreateLaunchTemplate",
        "ec2:CreateLaunchTemplateVersion",
        "ec2:CreateNatGateway",
        "ec2:CreateRoute",
        "ec2:CreateRouteTable",
        "ec2:CreateSecurityGroup",
        "ec2:CreateSubnet",
        "ec2:CreateTags",
        "ec2:CreateVolume",
        "ec2:CreateVpc",
        "ec2:CreateVpcEndpoint",
        "ec2:DeleteDhcpOptions",
        "ec2:DeleteFleets",
        "ec2:DeleteInternetGateway",
        "ec2:DeleteLaunchTemplate",
        "ec2:DeleteLaunchTemplateVersions",
        "ec2:DeleteNatGateway",
        "ec2:DeleteRoute",
        "ec2:DeleteRouteTable",
        "ec2:DeleteSecurityGroup",
        "ec2:DeleteSubnet",
        "ec2:DeleteTags",
        "ec2:DeleteVolume",
        "ec2:DeleteVpc",
        "ec2:DeleteVpcEndpoints",
        "ec2:DescribeAvailabilityZones",
        "ec2:DescribeFleetHistory",
        "ec2:DescribeFleetInstances",
        "ec2:DescribeFleets",
        "ec2:DescribeIamInstanceProfileAssociations",
        "ec2:DescribeInstanceStatus",
        "ec2:DescribeInstances",
        "ec2:DescribeInternetGateways",
        "ec2:DescribeLaunchTemplates",
        "ec2:DescribeLaunchTemplateVersions",
        "ec2:DescribeNatGateways",
        "ec2:DescribePrefixLists",
        "ec2:DescribeReservedInstancesOfferings",
        "ec2:DescribeRouteTables",
        "ec2:DescribeSecurityGroups",
        "ec2:DescribeSpotInstanceRequests",
        "ec2:DescribeSpotPriceHistory",
        "ec2:DescribeSubnets",
        "ec2:DescribeVolumes",
        "ec2:DescribeVpcs",
        "ec2:DetachInternetGateway",
        "ec2:DisassociateIamInstanceProfile",
        "ec2:DisassociateRouteTable",
        "ec2:GetLaunchTemplateData",
        "ec2:GetSpotPlacementScores",
        "ec2:ModifyFleet",
        "ec2:ModifyLaunchTemplate",
        "ec2:ModifyVpcAttribute",
        "ec2:ReleaseAddress",
        "ec2:ReplaceIamInstanceProfileAssociation",
        "ec2:RequestSpotInstances",
        "ec2:RevokeSecurityGroupEgress",
        "ec2:RevokeSecurityGroupIngress",
        "ec2:RunInstances",
        "ec2:TerminateInstances"
      ],
      "Resource": [
        "*"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "iam:CreateServiceLinkedRole",
        "iam:PutRolePolicy"
      ],
      "Resource": "arn:aws:iam::*:role/aws-service-role/spot.amazonaws.com/AWSServiceRoleForEC2Spot",
      "Condition": {
        "StringLike": {
          "iam:AWSServiceName": "spot.amazonaws.com"
        }
      }
    }
  ]
}'
```
::alert[ここでは Databricks が作成する VPC 内にワークスペースを展開するデフォルトの設定を適用しています。自身で管理する VPC を用いたり、制限を加えたい場合は[こちらのドキュメント](https://docs.databricks.com/administration-guide/account-settings-e2/credentials.html#step-2-create-an-access-policy)を参照してください。]{type=info}

### Databricks ワークスペースのルートストレージ用の S3 バケットを作成

次に、Databricks ワークスペースのルートストレージ用の S3 バケットを作成します。

1. 以下のコマンドの `<!!!your-name!!!>` をご自身のお名前等に置き換えた上で実行し、S3 バケットを作成してください。S3 バケットの名前は世界中で一意である必要があります。
```bash:
aws s3 mb s3://databricks-root-storage-<!!!your-name!!!> --region us-east-1
```
::alert[バージニア北部でないリージョンで作業している場合は `us-east-1` を適切なリージョン名に書き換えてください]{type=info}
2. 以下のコマンドの `<!!!your-name!!!>` (3箇所) および `<!!!databricks-account-id!!!>` (1箇所、前のセクションでコピーした 1abc23de-e4ed-56d7-ae89-abc12d345e60 のような文字列を入れる) を書き換えた上で実行し、バケットポリシーを設定してください。
```bash:
aws s3api put-bucket-policy --bucket databricks-root-storage-<!!!your-name!!!> --policy \
'{
 "Version": "2012-10-17",
 "Statement": [
  {
   "Sid": "Grant Databricks Access",
   "Effect": "Allow",
   "Principal": {
    "AWS": "arn:aws:iam::414351767826:root"
   },
   "Action": [
    "s3:GetObject",
    "s3:GetObjectVersion",
    "s3:PutObject",
    "s3:DeleteObject",
    "s3:ListBucket",
    "s3:GetBucketLocation"
   ],
   "Resource": [
    "arn:aws:s3:::databricks-root-storage-<!!!your-name!!!>/*",
    "arn:aws:s3:::databricks-root-storage-<!!!your-name!!!>"
   ],
   "Condition": {
    "StringEquals": {
     "aws:PrincipalTag/DatabricksAccountId": [
      "<!!!databricks-account-id!!!>"
     ]
    }
   }
  }
 ]
}'
```

### Credential configuration の作成

前のステップで作成した IAM のクロスアカウントロールを Databricks に登録していきます。

1. [Databricks 管理コンソール](https://accounts.cloud.databricks.com/)の左ペインの「Cloud resources」をクリックしてください。
![Select Cloud Resources](/static/00-prerequisites/cloud-resources.png)
2. 「Credential configuration」タブの「Add credential configuration」ボタンをクリックします。
3. 「Credential configuration name」には任意の名前 (例: `workshop-credential-configuration`) を入力し、「Role ARN」には `arn:aws:iam::<!!!aws-account-id!!!>:role/databricks-cross-account-role` を入力し、「Add」ボタンをクリックしてください。
![Setup credential configuration](/static/00-prerequisites/add-credential-configuration.png)

### Storage configuration の作成

続いて、先ほど作成した S3 バケットの情報を Databricks に登録していきます。

1. [Databricks 管理コンソール](https://accounts.cloud.databricks.com/)の左ペインの「Cloud resources」をクリックしてください。
2. 「Storage configuration」タブの「Add storage configuration」ボタンをクリックします。
3. 「Storage configuration name」には任意の名前 (例: `workshop-storage-configuration`) を入力し、「Bucket name」には先ほど作成した S3 バケットの名前 (例: `databricks-root-storage-<!!!your-name!!!>`) を入力し、「Add」ボタンをクリックしてください。
![Setup storage configuration](/static/00-prerequisites/add-storage-configuration.png)

### Databricks ワークスペースの作成

作成した Credential と Storage の構成情報を利用してワークスペースを作成します。

::alert[ワークスペースのプロビジョニング時に VPC が作成されます。利用している AWS アカウントのバージニア北部 (us-east-1) リージョンもしくはその他作業中のリージョンで VPC 数が上限に達していないか、あらかじめ確認してください。]{type=warning}

1. [Databricks 管理コンソール](https://accounts.cloud.databricks.com/)の左ペインの「Workspaces」をクリックしてください。
2. 画面右上の「Create workspace」をクリックしてください。もし、QuickStart か Manual かを選択するよう表示されたら **Manual** を選択してください。
3. 「Workspace name」に任意の名前 (例: `workshop`) を入力し、「Workspace URL」に任意の名前 (例: `workshop`) を入力し、「Region」では `N.Virginia (us-east-1)` を選択し、「credential configuration」では先ほど作成した構成 `workshop-credential-configuration` を選択し、「storage configuration」では先ほど作成した構成 `workshop-storage-configuration` を選択し、ページ下部の「Save」をクリックしてください。
![Create workspace](/static/00-prerequisites/create-workspace.png)
::alert[サブスクリプションのプランによっては Workspace URL を入力する項目がないなど、画面が多少異なります。]{type=warning}

これで自動的にワークスペースのプロビジョニングが始まります。
ワークスペースのリストからステータスを確認し、Provisioning から Running に変われば準備完了です。
通常、プロビジョニングは5分程度で完了します。

メールでワークスペースの URL が届くのでアクセスし、ログインしてください。
ログイン名およびパスワードは管理コンソールにログインするときのものと同じです。

## 参考文献

- [Create an IAM role for workspace deployment](https://docs.databricks.com/administration-guide/account-settings-e2/credentials.html)
- [Create an S3 bucket for workspace deployment](https://docs.databricks.com/administration-guide/account-settings-e2/storage.html)
- [Create a workspace using the account console](https://docs.databricks.com/administration-guide/workspace/create-workspace.html)
