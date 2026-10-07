import json
from config.configure_logger import configure_logger

logger = configure_logger(__name__)


def generate_return_response(status_code: int, body: str) -> dict:
    logger.debug(
        "Generating return response with status code %d and body: %s", status_code, body
    )
    return {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
        },
        "body": json.dumps({"message": body}),
    }
