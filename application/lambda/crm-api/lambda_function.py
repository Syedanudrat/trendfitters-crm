import json


def lambda_handler(event, context):
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps({
            "message": "TrendFitters CRM API is running!",
            "service": "CRM",
            "status": "healthy"
        })
    }