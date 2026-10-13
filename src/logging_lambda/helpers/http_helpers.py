import json

def generate_return_response(status_code: int, body: str) -> dict:
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps({"message": body}),
    }
