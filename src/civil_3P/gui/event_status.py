from __future__ import annotations

from enum import StrEnum


class EventStatus(StrEnum):
    SUCCESS = "success"
    FAILURE = "failure"
    WARNING = "warning"
