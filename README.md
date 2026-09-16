Serverless API on AWS Lambda, deployed with Terraform

A small Python API running on AWS Lambda, with the whole environment defined in Terraform. No part of this was clicked together in the AWS console.

What it deploys

Five resources, all from main.tf:

An IAM role the Lambda function assumes, scoped so only the Lambda service can use it
A permission attachment granting the role CloudWatch logging and nothing else
The Lambda function itself, packaged from the app/ directory
A public function URL
A resource-based permission allowing invocation through that URL
The application

app/main.py is a Lambda handler with two routes. /health returns a status check, anything else returns a greeting. Deliberately small, since the point of this project is the infrastructure around it rather than the application logic.

Running it

Requires Terraform and AWS credentials configured locally.

terraform init
terraform apply

Terraform prints the function URL as api_url when it finishes. To tear it down, run terraform destroy.

Tests
pip install pytest
pytest

Three tests cover the handler: the health route, the default route, and an event arriving with no rawPath at all, which the handler falls back on. They run automatically on every push through GitHub Actions.

Decisions

Terraform rather than the console. Clicking through the AWS console produces infrastructure nobody can review, reproduce or explain six months later. Defining it in code means the whole environment can be destroyed and rebuilt identically, changes go through the same review as application code, and the configuration is its own documentation.

The execution role does one thing. It has AWSLambdaBasicExecutionRole and nothing else, which is CloudWatch logging only. The function doesn't touch S3, a database or any other service, so it has no permission to. If it ever needs more, that becomes a deliberate change rather than an existing hole.

The trust policy names one principal. lambda.amazonaws.com and nothing else. A role is only as safe as the list of things allowed to assume it, and leaving that open is a quieter mistake than over-granting permissions, because nothing fails to draw attention to it.

The 403. The public URL returned 403 while the function itself was fine. Working that out meant invoking the function directly through the CLI first, which proved the code was sound and moved the problem to the access path in front of it. From there it was three separate layers: the URL's auth type, the resource-based policy saying who may invoke it, and an account-level restriction underneath both. All three have to agree before a request gets through, and AWS returns the same 403 regardless of which one refused you.

What I'd do differently

Use API Gateway rather than a function URL if this needed to grow. Function URLs are the simplest way to expose a Lambda, but they have no routing, no request validation and no throttling, all of which you'd want on anything real.

Write a custom inline policy instead of attaching the AWS managed one. AWSLambdaBasicExecutionRole is already minimal, but writing the permissions out makes the intent explicit rather than depending on what AWS decides that policy contains.