"""Configure logging for the application."""

import logging
import os
from typing import Optional
import json
from datetime import datetime, timezone

PROD = "prod"

class JsonFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        payload = {
            "timestamp": datetime.fromtimestamp(
                record.created, timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "external_route": getattr(record, "external_route", None),
            "journey_id": getattr(record, "journey_id", None),
            "lambda_request_id": getattr(record, "lambda_request_id", None),
        }
        if record.exc_info:
            payload["exception"] = self.formatException(record.exc_info)
        return json.dumps(payload, default=str)

def configure_logger(logger_name: Optional[str] = None) -> logging.Logger:
    """
    Configure and return a logger. If logger_name is not provided,
    returns the root logger.
    """
    logger = logging.getLogger(logger_name)

    resource_id = os.environ.get("ENVIRONMENT") or "dev"

    if resource_id.lower() == PROD.lower():
        logger.setLevel(logging.WARN)
    else:
        logger.setLevel(logging.DEBUG)

    # Prevent adding multiple handlers in interactive environments
    if not logger.handlers:
        handler = logging.StreamHandler()
        logger.addHandler(handler)

    for handler in logger.handlers:
        handler.setFormatter(JsonFormatter())
    logger.propagate = False

    return logger
