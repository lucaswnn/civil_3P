from __future__ import annotations

from enum import StrEnum


class ElementType(StrEnum):
    BAR_1D = "bar_1d"
    SHELL_2D = "shell_2d"


class ResultLocation(StrEnum):
    ELEMENT = "element"
    NODE = "node"


class VisualizationMode(StrEnum):
    ELEMENT = "element"
    NODE_AVERAGED = "node_averaged"
    NODE_RAW = "node_raw"


class TaskType(StrEnum):
    CHECK = "check"
    DESIGN = "design"
