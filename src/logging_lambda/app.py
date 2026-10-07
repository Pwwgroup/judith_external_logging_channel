from config.configure_logger import configure_logger
from models.log_event import LogEvent
from helpers.http_helpers import generate_return_response

import json

logger = configure_logger(__name__)


def handler(event, context):
    lambda_request_id = context.aws_request_id
    del context

    event_body = event.get("body", None)
    if not event_body:
        logger.error("No body in event")
        return generate_return_response(400, "No body in event")

    try:
        log_body = LogEvent.from_event(json.loads(event_body))
    except Exception:
        logger.error(
            f"JSON Loading error for event body: {event_body}",
            extra={"lambda_request_id": lambda_request_id},
        )
        return generate_return_response(400, "Invalid Request Body")

    log_message = log_body.message
    log_route = log_body.route
    log_id = log_body.id

    extra_log_entries = {
        "external_route": log_route,
        "journey_id": log_id,
        "lambda_request_id": lambda_request_id,
    }

    match log_body.state:
        case "error":
            logger.error(log_message, extra=extra_log_entries)
        case "warning":
            logger.warning(log_message, extra=extra_log_entries)
        case "info":
            logger.info(log_message, extra=extra_log_entries)
        case "debug":
            logger.debug(log_message, extra=extra_log_entries)
        case _:
            logger.error("No log state given", extra=extra_log_entries)
            return generate_return_response(404, "No log state given")
    return generate_return_response(200, "Successfully posted log")
