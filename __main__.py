"""An AWS Python Pulumi program"""

import pulumi
import pulumi_archive as archive
import pulumi_aws as aws

# Create Lambda function
assume_role = aws.iam.get_policy_document(
    statements=[
        aws.iam.GetPolicyDocumentStatementArgs(
            effect="Allow",
            principals=[
                aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                    type="Service",
                    identifiers=["lambda.amazonaws.com"],
                ),
                aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                    type="Service",
                    identifiers=["dynamodb.amazonaws.com"],
                )
            ],
            actions=["sts:AssumeRole"],
        ),
    ]
)
iam_for_lambda = aws.iam.Role("iam_for_lambda",
    name="iam_for_lambda",
    assume_role_policy=assume_role.json)

# Attach the AdministratorAccess managed policy to the role
# This is not best practice but I just want to keep it simple
admin_policy_attachment = aws.iam.RolePolicyAttachment("lambda-admin-policy-attachment",
    role=iam_for_lambda.name,
    policy_arn="arn:aws:iam::aws:policy/AdministratorAccess"
)

lambda_ = archive.get_file(type="zip",
    source_file="lambda_function.py", # the actual code to be run on the Lambda
    output_path="lambda_function_payload.zip")

test_lambda = aws.lambda_.Function("pulumi_uploader_lambda",
    code=pulumi.FileArchive("lambda_function_payload.zip"),
    name="pulumi_uploader_lambda",
    role=iam_for_lambda.arn,
    handler="lambda_function.lambda_handler",
    source_code_hash=lambda_.output_base64sha256,
    runtime=aws.lambda_.Runtime.PYTHON3D12,
)

# Create DynamoDB Table
dynamodb_table = aws.dynamodb.Table("basic-dynamodb-table",
    name="Uploads",
    billing_mode="PROVISIONED",
    read_capacity=20,
    write_capacity=20,
    hash_key="file_name",
    range_key="timestamp",
    attributes=[
        aws.dynamodb.TableAttributeArgs(
            name="file_name",
            type="S",
        ),
        aws.dynamodb.TableAttributeArgs(
            name="timestamp",
            type="S",
        ),
    ],
    ttl=aws.dynamodb.TableTtlArgs(
        attribute_name="TimeToExist",
        enabled=False,
    ),
    tags={
        "Name": "uploads-table",
        "Environment": "dev",
    })

# Create S3 Bucket
bucket = aws.s3.Bucket('pulumi-serverless-app')

allow_bucket = aws.lambda_.Permission("allow_bucket",
    statement_id="AllowExecutionFromS3Bucket",
    action="lambda:InvokeFunction",
    function=test_lambda.arn,
    principal="s3.amazonaws.com",
    source_arn=bucket.arn)
bucket_notification = aws.s3.BucketNotification("bucket_notification",
    bucket=bucket.id,
    lambda_functions=[aws.s3.BucketNotificationLambdaFunctionArgs(
        lambda_function_arn=test_lambda.arn,
        events=["s3:ObjectCreated:*"],
    )],
    opts=pulumi.ResourceOptions(depends_on=[allow_bucket]))


# Export the name of the bucket
pulumi.export('bucket_name', bucket.id)

# Export the name of the Lambda function
pulumi.export('lambda_name', lambda_.id)

# Export the name of the DynamoDB table
pulumi.export('table_name', dynamodb_table.id)
