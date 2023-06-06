---
title: "MLflow Model Registry から Amazon SageMaker にデプロイ"
weight: 41
---

このラボでは、MLflow のモデルを Amazon SageMaker にデプロイする方法を学びます。
まず、Databricks のノートブックから直接モデルをデプロイできるように、クラスターに対して[インスタンスプロファイル](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/iam-roles-for-amazon-ec2.html)を設定します。

## 事前準備: インスタンスプロファイルをクラスターにアタッチ

Databricks クラスターは Amazon EC2 の上で構成されています。
クラスター上で動いているノートブックから SageMaker を操作できるようにするには、EC2 に対して SageMaker 周りの権限を与えた IAM ロールをアタッチする必要があります。
インスタンスプロファイルは IAM ロールのコンテナであり、インスタンスの起動時に EC2 インスタンスにロール情報を渡すためのコネクターの役割をします。

### Step 1: IAM ロールの作成

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

### Step 2: 作成した IAM ロールの信頼関係を更新

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

### Step 3: 

## 参考文献

- [Set up AWS authentication for SageMaker deployment](https://docs.databricks.com/administration-guide/cloud-configurations/aws/sagemaker.html)
