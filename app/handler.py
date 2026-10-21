"""Image Intake - S3 uploads/ object create writes metadata to DynamoDB."""
import json
import os
import urllib.parse

TABLE_NAME = os.environ.get("TABLE_NAME", "")
APP_VERSION = os.environ.get("APP_VERSION", "dev")

_table = None


def table():
    global _table
    if _table is None:
        import boto3

        _table = boto3.resource("dynamodb").Table(TABLE_NAME)
    return _table


def lambda_handler(event, context):
    written = []
    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = urllib.parse.unquote_plus(record["s3"]["object"]["key"])
        size = int(record["s3"]["object"].get("size") or 0)
        if not key.startswith("uploads/"):
            continue
        content_type = "application/octet-stream"
        try:
            import boto3

            head = boto3.client("s3").head_object(Bucket=bucket, Key=key)
            content_type = head.get("ContentType") or content_type
            size = int(head.get("ContentLength") or size)
        except Exception:
            pass
        item = {
            "object_key": key,
            "size": size,
            "content_type": content_type,
            "bucket": bucket,
            "version": APP_VERSION,
        }
        table().put_item(Item=item)
        written.append(key)
    return {"ok": True, "written": written, "version": APP_VERSION}
