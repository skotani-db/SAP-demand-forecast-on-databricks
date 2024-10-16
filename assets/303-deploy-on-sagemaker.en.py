# Databricks notebook source
# MAGIC %md
# MAGIC # Deploying from MLflow Model Registry to Amazon SageMaker

# COMMAND ----------

# MAGIC %md
# MAGIC Store in variables the URI of the model that you registered in the MLflow Model Registry and transitioned to Production, and the URL of the Amazon ECR container repository.

# COMMAND ----------

# MAGIC %pip install boto3 -q

# COMMAND ----------

import boto3

account_id = boto3.client("sts").get_caller_identity().get("Account")

# Change the region name as needed.
region = "us-east-1"
# !!! Please change it to the model name registered in the Model Registry!!!
model_uri = "models:/kazmot-sales-predict/1"
# Container image created with the mlflow sagemaker build-and-push-container command
image_ecr_url = f"{account_id}.dkr.ecr.{region}.amazonaws.com/mlflow-pyfunc:2.5.0"

# COMMAND ----------

# MAGIC %md
# MAGIC Use the `mlflow.deployments` module to get a client for deployment in SageMaker. Executing the `create_deployment` method will start the deployment of the SageMaker inference endpoint. The API reference for `SageMakerDeploymentClient` is here.
# MAGIC
# MAGIC > In this example, the number of instances is `1` and the instance type is `ml.m4.xlarge`. By using two or more instances, they are automatically distributed across multiple Availability Zones (AZs), improving the availability of the inference endpoint. For production use, a multi-AZ configuration is recommended. In addition, with SageMaker real-time inference endpoints, you can set auto-scaling according to load and preset timing. For more information, see "[Automatically Scale Amazon SageMaker Modesl](https://docs.aws.amazon.com/sagemaker/latest/dg/endpoint-auto-scaling.html)" in the documentation.

# COMMAND ----------

import mlflow.deployments
 
deployment_name = "sales-predict-endpoint"
 
deployment_client = mlflow.deployments.get_deploy_client("sagemaker:/" + region)
deployment_client.create_deployment(
    name=deployment_name,
    model_uri=model_uri,
    config={
      "image_url": image_ecr_url,
      "instance_count": 1,
      "instance_type": "ml.m4.xlarge",
    }
)

# COMMAND ----------

deployment_info = deployment_client.get_deployment(name=deployment_name)
print(f"MLflow SageMaker Deployment status is: {deployment_info['EndpointStatus']}")

# COMMAND ----------

# MAGIC %md
# MAGIC Once the inference endpoint deployment is complete, return to the workshop page and proceed to the next lesson, “Lab 4: Visualization Dashboard Development.”

# COMMAND ----------

# MAGIC %md
# MAGIC ## LICENSE
# MAGIC MIT No Attribution
# MAGIC
# MAGIC Copyright 2023 Amazon Web Services Japan G.K.
# MAGIC
# MAGIC Permission is hereby granted, free of charge, to any person obtaining a copy of this
# MAGIC software and associated documentation files (the "Software"), to deal in the Software
# MAGIC without restriction, including without limitation the rights to use, copy, modify,
# MAGIC merge, publish, distribute, sublicense, and/or sell copies of the Software, and to
# MAGIC permit persons to whom the Software is furnished to do so.
# MAGIC
# MAGIC THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED,
# MAGIC INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A
# MAGIC PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# MAGIC HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# MAGIC OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# MAGIC SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
