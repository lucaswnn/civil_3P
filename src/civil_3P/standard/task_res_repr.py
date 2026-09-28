from __future__ import annotations

from enum import StrEnum


class TaskBarResCols(StrEnum):
    ELEMENT = "element"
    STATION = "station"
    CASE = "case"
    VALUE = "value"


class TaskShellResCols(StrEnum):
    ELEMENT = "element"
    NODE = "node"
    CASE = "case"
    VALUE = "value"


class TaskNodeResCols(StrEnum):
    NODE = "node"
    CASE = "case"
    VALUE = "value"
