from dataclasses import dataclass
from typing import Any

MESSAGE_STATES = ["error", "info", "warning", "debug"]


@dataclass
class LogEvent:
    state: str
    message: str
    route: str
    id: str

    @classmethod
    def from_event(cls, event: dict[str, Any]):
        log_state = event.get("state", None)
        log_message = event.get("message", None)
        log_route = event.get("route", None)
        external_journey_id = event.get("journey_id", None)

        if not log_state or not log_message or not log_route:
            raise ValueError("Expected non-null values for state, message and route")

        if log_state not in MESSAGE_STATES:
            raise ValueError(
                f"Log state {log_state} is not in list of expected states: {MESSAGE_STATES}"
            )

        return cls(state=log_state, message=log_message, route=log_route, id=external_journey_id)
