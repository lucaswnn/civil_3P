from enum import StrEnum


class ResultLocation(StrEnum):
    ELEMENT = "element"
    NODE = "node"


class VisualizationMode(StrEnum):
    ELEMENT = "element"
    NODE_AVERAGED = "node_averaged"
    NODE_RAW = "node_raw"
