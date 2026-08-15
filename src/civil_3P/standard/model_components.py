from enum import StrEnum


class ModelComponents(StrEnum):
    ELEMENTS_1D = "elements_1d"
    ELEMENTS_2D = "elements_2d"
    NODES = "nodes"


class ModelNodeComponents(StrEnum):
    NODE_X = "node_x"
    NODE_Y = "node_y"
    NODE_Z = "node_z"


class ModelElement1DComponents(StrEnum):
    ELEMENT_1D_START_NODE = "element_1d_start"
    ELEMENT_1D_END_NODE = "element_1d_end"


class ModelElement2DComponents(StrEnum):
    ELEMENT_2D_NODES = "element_2d_nodes"
