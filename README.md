# Serverless API on AWS Lambda, deployed with Terraform

A small Python API running on AWS Lambda, with the whole environment defined in Terraform. No part of this was clicked together in the AWS console.

## What it deploys

Five resources, all from `main.tf`:

- An IAM role the Lambda function assumes, scoped so only the Lambda service can use it
- A permission attachment granting the role CloudWatch logging and nothing else
- The Lambda function itself, packaged from the `app/` directory
- A public function URL
- A resource-based permission allowing invocation through that URL

## The application

`app/main.py` is a Lambda handler with two routes. `/health` returns a status check, anything else returns a greeting. Deliberately small, since the point of this project is the infrastructure around it rather than the application logic.

## Running it
