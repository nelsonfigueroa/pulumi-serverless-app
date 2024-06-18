import boto3
import json

TABLE_NAME = "Uploads"


def lambda_handler(event, context):
    client = boto3.client("dynamodb", "us-west-1")

    # need to get file_name and add a timestamp, which should be generated on the fly. Unless its provided in the payload?
    # body = json.loads(event["body"])
    # event = json.loads(event)

    print(event)
    print(type(event))

    file_name = event["Records"][0]["s3"]["object"]["key"]
    timestamp = event["Records"][0]["eventTime"]

    client.put_item(
        TableName=TABLE_NAME,
        Item={
            "file_name": {"S": file_name},
            "timestamp": {"S": timestamp},
        },
    )

    print(f"File added to database: {file_name}: {timestamp}")
    return
