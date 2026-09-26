from __future__ import annotations

from enum import StrEnum


class ViewContentKind(StrEnum):
    NODE_POINTS = "node_points"
    ELEMENT_1D_PROFILE = "element_1d_profile"
    ELEMENT_2D_UNIFORM = "element_2d_uniform"
    ELEMENT_2D_SHARED_NODES = "element_2d_shared_nodes"
    ELEMENT_2D_ISOLATED_NODES = "element_2d_isolated_nodes"
