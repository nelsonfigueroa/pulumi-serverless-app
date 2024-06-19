# pulumi-serverless-app

For Pulumi interview. This is a serverless app consisting of a S3 bucket, Lambda function, and DynamoDB table. When a file is uploaded to the S3 bucket, the Lambda is triggered, which writes the filename and timestamp to a DynamoDB table.

The prompt is as follows:

Using Pulumi, create and deploy a serverless application that processes uploads to a storage bucket and builds an index of the files in a database table.

Use one of AWS, Azure, or Google Cloud and your language of choice.

At a minimum your Pulumi application code should consist of:
- A storage bucket
- A database table
- A serverless function that processes object uploads and writes the object key and a timestamp to the database table

You cannot use the Pulumi AWS SDK from within your serverless function. You must use the AWS SDK for Node, Python, or some other Pulumi supported language to write to the database.

Success criteria:
- Should be able to upload a file to the bucket and see the database entry get created

Serverless app that triggers a Lambda on S3 object upload and writes the filename and timestamp to a DynamoDB table.
