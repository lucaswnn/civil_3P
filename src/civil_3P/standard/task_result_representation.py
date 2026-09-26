from __future__ import annotations

from enum import StrEnum


class Task1DResultsColumns(StrEnum):
    ELEMENT = "element"
    STATION = "station"
    CASE = "case"
    VALUE = "value"


class Task2DResultsColumns(StrEnum):
    ELEMENT = "element"
    NODE = "node"
    CASE = "case"
    VALUE = "value"


class TaskNodeResultsColumns(StrEnum):
    NODE = "node"
    CASE = "case"
    VALUE = "value"
