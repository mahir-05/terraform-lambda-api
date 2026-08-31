import json


def handler(event, context):
    path = event.get("rawPath", "/")

    if path == "/health":
        body = {"status": "ok"}
    else:
        body = {"message": "Hello from Lambda"}

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps(body)
    }
